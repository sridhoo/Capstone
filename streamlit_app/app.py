# import streamlit as st
# import requests

# st.title("FitEats Meal Planner 🍽️")

# # User input fields
# diet_type = st.text_input("Enter your diet preferences (e.g., Vegan, 2000 calories)")
# generate_btn = st.button("Generate Meal Plan")

# if generate_btn:
#     if diet_type:
#         response = requests.post("http://localhost:5000/meal_plan", json={"preferences": diet_type})
#         meal_plan = response.json()["meal_plan"]
#         st.write("### Your Meal Plan")
#         st.write(meal_plan)
#     else:
#         st.warning("Please enter your diet preferences!")

# NUMBER 2
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

# NUMBER 2 UPDATED
# import streamlit as st
# import requests
# import time
# import matplotlib.pyplot as plt
# from utils.meal_parser import parse_meal_plan
# from components.editable_table import show_editable_meal_plan

# # 1. PAGE CONFIG
# st.set_page_config(
#     page_title="FitEats AI Meal Planner", 
#     page_icon="🥗",
#     layout="wide"
# )

# # 2. OLLAMA HELPER FUNCTIONS
# def is_ollama_running():
#     try:
#         return requests.get("http://localhost:11434", timeout=5).status_code == 200
#     except:
#         return False

# def generate_with_retry(prompt, max_retries=3):
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(
#                 "http://localhost:11434/api/generate",
#                 json={
#                     "model": "mistral",
#                     "prompt": prompt,
#                     "stream": False,
#                     "options": {"temperature": 0.7}
#                 },
#                 timeout=120
#             )
#             response.raise_for_status()
#             return response.json()["response"]
#         except Exception as e:
#             if attempt == max_retries - 1:
#                 raise
#             time.sleep(2 * (attempt + 1))

# # 3. STREAMLIT UI
# st.title("🥗 FitEats AI Meal Planner")
# st.write("Personalized meal plans with editable options powered by AI.")

# with st.form("meal_plan_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         age = st.number_input("Age", 10, 100, 25)
#         weight = st.number_input("Weight (kg)", 30, 200, 70)
#         goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
#     with col2:
#         height = st.number_input("Height (cm)", 100, 250, 170)
#         activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
#         days = st.slider("Plan Duration", 1, 7, 3)
    
#     preferences = st.text_input("Dietary Preferences", "High Protein")
#     submitted = st.form_submit_button("Generate Meal Plan")

# # 4. MEAL PLAN GENERATION
# if submitted:
#     if not is_ollama_running():
#         st.error("🚨 Ollama is not running! Please open a terminal and run:")
#         st.code("ollama serve")
#         st.stop()

#     # 4.1 Construct Strict Prompt
#     prompt = (
#         f"Generate a {days}-day meal plan. "
#         f"Each day should be labeled as 'Day X' (e.g., Day 1) on its own line. "
#         f"Each day should include:\n"
#         f"Breakfast: [description]\nLunch: [description]\nDinner: [description]\n"
#         f"Repeat this for each day. No extra text or explanation.\n\n"
#         f"User profile:\n"
#         f"Age: {age}\nWeight: {weight}kg\nHeight: {height}cm\n"
#         f"Activity Level: {activity}\nGoal: {goal}\nPreferences: {preferences}"
#     )

#     # 4.2 Generate Plan
#     with st.spinner("🍳 Cooking up your perfect meal plan..."):
#         try:
#             start_time = time.time()
#             raw_response = generate_with_retry(prompt)

#             # Show raw response for debugging
#             st.subheader("🧾 Raw AI Output")
#             st.code(raw_response, language="markdown")

#             meal_plan = parse_meal_plan(raw_response, days)

#             if not meal_plan:
#                 st.error("⚠️ Failed to parse the meal plan. Please try again.")
#             else:
#                 # Display structured plan
#                 st.success("✅ Here's your personalized meal plan:")
#                 for day, meals in meal_plan.items():
#                     with st.expander(day):
#                         for meal, desc in meals.items():
#                             st.markdown(f"**{meal}**: {desc}")

#                 # Editable Table
#                 st.divider()
#                 st.subheader("✏️ Make Edits to Your Plan")
#                 show_editable_meal_plan(meal_plan)

#                 if "updated_plan" in st.session_state:
#                     st.subheader("📋 Updated Plan Preview")
#                     st.dataframe(st.session_state["updated_plan"], use_container_width=True)

#                 # Nutrition Chart
#                 st.divider()
#                 st.subheader("📊 Macronutrient Breakdown (Sample)")
#                 fig, ax = plt.subplots()
#                 ax.pie([30, 40, 30], labels=["Protein", "Carbs", "Fats"], autopct="%1.1f%%", startangle=90)
#                 ax.axis("equal")
#                 st.pyplot(fig)

#                 st.caption(f"⏱️ Generated in {time.time() - start_time:.2f} seconds")

#         except Exception as e:
#             st.error(f"🚨 Error: {str(e)}")
#             st.markdown("""
#             **Troubleshooting Tips:**
#             1. Ensure `ollama serve` is running.
#             2. Make sure the model is available: `ollama pull mistral`
#             3. Check for any prompt formatting errors.
#             """)




# NUMBER 3
# import streamlit as st
# from meal_generator import generate_meal_plan_with_ollama
# import re

# st.set_page_config(page_title="FitEats Meal Planner", layout="centered")
# st.title("🍽️ FitEats AI Meal Planner")

# user_input = st.text_area("Describe your goals, allergies, or preferences:")
# days = st.slider("Select number of days", 1, 7, 3)

# if st.button("Generate Plan"):
#     st.info("Generating your meal plan. This may take up to 2–3 minutes... ⏳")

#     meal_plan = generate_meal_plan_with_ollama(user_input, days)
    
#     if "⚠️" in meal_plan:
#         st.error(meal_plan)
#     else:
#         st.success("✅ Here's your personalized meal plan!")
#         days_output = re.split(r'Day \d+:', meal_plan)
#         for i, content in enumerate(days_output[1:], start=1):
#             st.markdown(f"### Day {i}")
#             st.markdown(content.strip().replace("-", "•"))

#         with st.expander("📊 Macronutrient Breakdown (Sample)"):
#             st.write("Protein: 30% | Carbs: 45% | Fats: 25%")
