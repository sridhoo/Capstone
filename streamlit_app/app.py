import streamlit as st
import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
from utils.meal_parser import parse_meal_plan
from components.editable_table import show_editable_meal_plan

st.set_page_config(page_title="AI Meal Planner", page_icon="🥗", layout="wide")

st.title("🥗 AI Meal Planner")
st.write("Personalized meal plans with editable options powered by AI.")

with st.form("profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 10, 100, 25)
        weight = st.number_input("Weight (kg)", 30, 200, 70)
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
    with col2:
        height = st.number_input("Height (cm)", 100, 250, 170)
        activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
        days = st.slider("Plan Duration", 1, 7, 3)

    preferences = st.text_input("Preferences (e.g. Vegan, Low Carb, High Protein)", "High Protein")
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    st.info("Generating meal plan, This may take a while...")
    start_time = time.time()

    prompt = (
        f"Create a {days}-day meal plan for a person with these details:\n"
        f"Age: {age}, Weight: {weight}kg, Height: {height}cm, Activity Level: {activity}, "
        f"Goal: {goal}, Preferences: {preferences}.\n\n"
        f"For each day, list:\n"
        f"Day X\n"
        f"Breakfast: <meal>\n"
        f"Lunch: <meal>\n"
        f"Dinner: <meal>\n\n"
        f"Follow this exact format strictly. Do not add anything extra like calorie counts."
    )

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        raw_text = response.json()["response"]
        st.code(raw_text)  # Shows what Mistral actually gave back
        meal_plan = parse_meal_plan(raw_text, days)

        if not meal_plan:
         st.error("⚠️ No meal plan generated. Please try again.")
        else:
            # ... display meal plan ...
            st.divider()
            st.subheader("✏️ Make Changes to Your Plan")
            show_editable_meal_plan(meal_plan)  # This calls our updated component
            
            # Display in a structured format
            for day in sorted(meal_plan.keys()):
                with st.expander(f"📅 {day}", expanded=True):
                    cols = st.columns(3)
                    
                    meals = meal_plan[day]
                    for i, meal_type in enumerate(["Breakfast", "Lunch", "Dinner"]):
                        with cols[i]:
                            st.markdown(f"**{meal_type}**")
                            if meal_type in meals and meals[meal_type]:
                                st.markdown(meals[meal_type])
                            else:
                                st.warning("No meal generated")
            
            st.divider()
            st.subheader("✏️ Make Changes to Your Plan")
            
            # Pass the meal plan to the editable table
            show_editable_meal_plan(meal_plan)
            
            # Show updated plan if available
            if "updated_plan" in st.session_state:
                st.subheader("📋 Updated Plan Preview")
                updated_df = pd.DataFrame([
                    {"Day": day, "Meal": meal, "Description": desc}
                    for day, meals in st.session_state["updated_plan"].items()
                    for meal, desc in meals.items()
                ])
                st.dataframe(updated_df, use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("📊 Macronutrient Breakdown (Sample)")

            fig, ax = plt.subplots()
            labels = ['Protein', 'Carbs', 'Fats']
            sizes = [30, 45, 25]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            st.caption(f"⏱️ Generated in {time.time() - start_time:.2f}s")

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Connection Error: {e}")
    except ValueError as e:
        st.error(f"🚨 JSON Parsing Error: {e}")
    except Exception as e:
        st.error(f"🚨 Unexpected Error: {e}")

