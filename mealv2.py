# import streamlit as st
# import requests
# import pandas as pd
# import matplotlib.pyplot as plt
# import speech_recognition as sr  # <--- Add this line for speech-to-text

# # --- USDA API Setup ---
# USDA_API_KEY = '9vFLEh9HWxgZlFZ3a95L2IFzVqmygqT90cindN6f'  # Replace with your USDA API Key
# USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# # --- Calorie Calculator ---
# def calculate_calories(goal, weight, height, age, gender):
#     if gender == "Male":
#         bmr = 10 * weight + 6.25 * height - 5 * age + 5
#     else:
#         bmr = 10 * weight + 6.25 * height - 5 * age - 161

#     if goal == "Weight loss":
#         return bmr - 500
#     elif goal == "Weight gain" or goal == "Muscle building":
#         return bmr + 500
#     else:
#         return bmr

# # --- Search Food from USDA ---
# def search_food(item):
#     params = {
#         "api_key": USDA_API_KEY,
#         "query": item,
#         "pageSize": 1
#     }
#     response = requests.get(USDA_SEARCH_URL, params=params)
#     data = response.json()

#     if data.get("foods"):
#         food = data["foods"][0]
#         nutrients = food.get("foodNutrients", [])
#         calories = next((nutrient["value"] for nutrient in nutrients if nutrient["nutrientName"] == "Energy"), "Unknown")
#         return {
#             "description": food["description"],
#             "calories": calories
#         }
#     else:
#         return {"description": item, "calories": "Unknown"}

# # --- Streamlit UI ---
# st.set_page_config(page_title="AI Meal Planner", page_icon="🥗", layout="centered")

# st.title("🥗 AI Meal Planner (Interactive) + 🎤 Speech to Text")

# # --- Input Form ---
# with st.form("meal_form"):
#     age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
#     height = st.number_input("Your Height (cm)", min_value=100, max_value=250, step=1)
#     weight = st.number_input("Your Weight (kg)", min_value=30, max_value=200, step=1)
#     gender = st.selectbox("Your Gender", ["Male", "Female"])
    
#     goal = st.radio("What are your health and fitness goals?", 
#                     ["Weight loss", "Weight gain", "Muscle building", "Maintain current weight"])
    
#     cuisine = st.selectbox("What type of cuisines do you enjoy?", 
#                            ["Indian", "Italian", "Mexican", "American", "Chinese", "Other"])
    
#     meal_type = st.selectbox("Include Meals For:", 
#                              ["Breakfast", "Lunch", "Dinner", "Snacks", "All Meals"])
    
#     submitted = st.form_submit_button("Generate Meal Plan")

# # --- After Submit ---
# if submitted:
#     st.success("Generating your interactive meal plan... 🍴")
    
#     daily_calories = calculate_calories(goal, weight, height, age, gender)
    
#     # Set preferences
#     if cuisine == "Indian":
#         preferences = ["dal", "grilled chicken", "vegetable curry", "chapati", "sambar"]
#     elif cuisine == "Italian":
#         preferences = ["pasta", "grilled chicken", "salad", "risotto"]
#     elif cuisine == "Mexican":
#         preferences = ["tacos", "grilled vegetables", "black beans"]
#     elif cuisine == "American":
#         preferences = ["burger", "grilled fish", "steak", "mashed potatoes"]
#     elif cuisine == "Chinese":
#         preferences = ["noodles", "fried rice", "stir fry vegetables"]
#     else:
#         preferences = ["salad", "grilled chicken", "vegetable soup"]

#     calories_per_meal = daily_calories / len(preferences)

#     # Collect Meal Info
#     meal_data = []
#     for item in preferences:
#         food_info = search_food(item)
#         meal_data.append({
#             "Meal": food_info["description"],
#             "Target Calories": int(calories_per_meal),
#             "Actual Calories": food_info["calories"]
#         })

#     meal_df = pd.DataFrame(meal_data)

#     # 🎯 Display Summary
#     st.header(f"🎯 Daily Calorie Goal: {int(daily_calories)} kcal")

#     # 🍽️ Show Meal Plan as Expanders
#     st.subheader("🍽️ Your Meal Plan:")
#     for idx, row in meal_df.iterrows():
#         with st.expander(f"🍴 {row['Meal']}"):
#             st.write(f"🔹 **Target Calories:** {row['Target Calories']} kcal")
#             st.write(f"🔹 **Approx Calories (USDA):** {row['Actual Calories']} kcal")

#     # 📊 Show Bar Chart
#     st.subheader("📊 Calories Per Meal")
#     fig, ax = plt.subplots()
#     ax.bar(meal_df['Meal'], meal_df['Actual Calories'])
#     plt.xticks(rotation=45, ha='right')
#     plt.ylabel("Calories")
#     plt.title("Calories per Meal")
#     st.pyplot(fig)

#     # 📥 Download Meal Plan
#     st.download_button(
#         label="📥 Download Meal Plan as CSV",
#         data=meal_df.to_csv(index=False).encode('utf-8'),
#         file_name="meal_plan.csv",
#         mime="text/csv",
#     )

#     # ======================
#     # 🎤 Speech-to-Text Section
#     # ======================
#     # 🎤 Speech-to-Text Section with Button
# st.header("🎙️ Speak to Search or Add Foods")

# recognizer = sr.Recognizer()

# # Create a button to activate microphone
# if st.button("🎙️ Click Here to Speak"):
#     try:
#         with sr.Microphone() as source:
#             st.info("Listening... Please speak clearly.")
#             audio = recognizer.listen(source)
#             st.success("Done listening! Recognizing...")

#             # Recognize the speech
#             text = recognizer.recognize_google(audio)
#             st.subheader("📝 Recognized Text:")
#             st.success(f"{text}")

#             # ➡️ Here you can optionally use the text for searching foods dynamically
#             # Example: search_food(text)

#     except sr.UnknownValueError:
#         st.error("❌ Sorry, I could not understand your speech.")
#     except sr.RequestError:
#         st.error("❌ Could not connect to the speech recognition service.")
