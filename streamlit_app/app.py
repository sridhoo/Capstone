import streamlit as st
import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
from utils.meal_parser import parse_meal_plan
from components.editable_table import show_editable_meal_plan

st.set_page_config(page_title="AI Meal Planner", page_icon="🥗", layout="wide")

# Custom CSS for scrollable table
st.markdown("""
    <style>
    .stDataFrame {
        overflow-x: auto;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 AI Meal Planner")
st.write("Personalized meal plans with editable options powered by AI.")

# Initialize session state
if "meal_plan" not in st.session_state:
    st.session_state["meal_plan"] = None
if "generation_time" not in st.session_state:
    st.session_state["generation_time"] = None

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
    with st.status("Generating meal plan, please wait..."):
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
            response.raise_for_status()
            raw_text = response.json()["response"]
            st.code(raw_text, language="text")
            meal_plan = parse_meal_plan(raw_text, days)

            if not meal_plan or not any(meal_plan.values()):
                st.error("⚠️ No valid meal plan generated. Please try again.")
            else:
                st.session_state["meal_plan"] = meal_plan
                st.session_state["generation_time"] = time.time() - start_time

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API Connection Error: {e}")
            st.session_state["meal_plan"] = None
            st.session_state["generation_time"] = None
        except ValueError as e:
            st.error(f"🚨 JSON Parsing Error: {e}")
            st.session_state["meal_plan"] = None
            st.session_state["generation_time"] = None
        except Exception as e:
            st.error(f"🚨 Unexpected Error: {e}")
            st.session_state["meal_plan"] = None
            st.session_state["generation_time"] = None

# Display meal plan if available
if st.session_state["meal_plan"]:
    try:
        meal_plan = st.session_state["meal_plan"]
        st.divider()
        st.subheader("📅 Your Meal Plan")

        # Display meals
        for day in sorted(meal_plan.keys()):
            st.markdown(f"**{day}**")
            meals = meal_plan[day]
            cols = st.columns(3)
            for i, meal_type in enumerate(["Breakfast", "Lunch", "Dinner"]):
                with cols[i]:
                    st.markdown(f"**{meal_type}**")
                    description = meals.get(meal_type, "No meal generated")
                    if description and description != "No meal generated":
                        st.markdown(description)
                    else:
                        st.warning("No meal generated")

        st.divider()
        st.subheader("✏️ Edit Your Plan")
        show_editable_meal_plan(meal_plan, key="main_meal_plan_editor")

        st.divider()
        st.subheader("📊 Macronutrient Breakdown (Sample)")
        fig, ax = plt.subplots()
        labels = ['Protein', 'Carbs', 'Fats']
        sizes = [30, 45, 25]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        if st.session_state["generation_time"]:
            st.caption(f"⏱️ Generated in {st.session_state['generation_time']:.2f}s")

    except Exception as e:
        st.error(f"🚨 Error displaying meal plan: {e}")

