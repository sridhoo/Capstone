import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Constants
USDA_API_KEY = "9vFLEh9HWxgZlFZ3a95L2IFzVqmygqT90cindN6f"
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Title
st.title("🍽️ FitEats: AI-Powered Meal Planner")

# Sidebar - User Inputs
st.sidebar.header("Your Info")
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=175)
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
activity_level = st.sidebar.selectbox(
    "Activity Level",
    ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"]
)
goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Lose Weight", "Maintain Weight", "Gain Muscle"]
)

cuisine = st.sidebar.selectbox(
    "Preferred Cuisine",
    ["Any", "Indian", "Italian", "Mexican", "American", "Chinese"]
)

meal_type = st.sidebar.selectbox(
    "Meal Type",
    ["All Meals", "Breakfast", "Lunch", "Dinner", "Snacks"]
)

# Function to calculate BMR and daily calories
def calculate_calories(weight, height, age, sex, activity_level, goal):
    if sex == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }

    calories = bmr * activity_multipliers[activity_level]

    if goal == "Lose Weight":
        calories -= 500
    elif goal == "Gain Muscle":
        calories += 300

    return round(calories)

# Get calories
daily_calories = calculate_calories(weight, height, age, sex, activity_level, goal)
st.subheader(f"🔥 Daily Calorie Target: {daily_calories} kcal")

# Meal options by type and cuisine
meal_options = {
    "Breakfast": {
        "Any": ["oatmeal", "eggs", "smoothie", "protein pancakes", "Greek yogurt"],
        "Indian": ["idli", "poha", "paratha", "upma"],
        "Italian": ["ricotta toast", "granola and yogurt", "mozzarella eggs"],
        "Mexican": ["breakfast tacos", "avocado toast", "huevos rancheros"],
        "American": ["eggs and toast", "pancakes", "breakfast burrito"],
        "Chinese": ["congee", "baozi", "soy milk with fried dough"]
    },
    "Lunch": {
        "Any": ["chicken wrap", "rice and beans", "grilled vegetables", "pasta salad"],
        "Indian": ["dal rice", "rajma", "grilled paneer with veggies"],
        "Italian": ["pasta primavera", "chicken risotto"],
        "Mexican": ["burrito bowl", "chicken enchiladas"],
        "American": ["grilled cheese", "turkey sandwich", "mac and cheese"],
        "Chinese": ["noodle bowl", "rice with tofu and broccoli"]
    },
    "Dinner": {
        "Any": ["salmon with veggies", "quinoa bowl", "stir fry", "chili"],
        "Indian": ["butter chicken", "vegetable biryani", "chapati and sabzi"],
        "Italian": ["spaghetti", "chicken parmesan", "pesto gnocchi"],
        "Mexican": ["fajitas", "stuffed peppers"],
        "American": ["steak and mashed potatoes", "baked chicken"],
        "Chinese": ["kung pao chicken", "fried rice"]
    },
    "Snacks": {
        "Any": ["protein bar", "fruit", "mixed nuts", "rice cakes", "boiled eggs"],
        "Indian": ["moong dal chaat", "roasted chickpeas"],
        "Italian": ["bruschetta", "olives and cheese"],
        "Mexican": ["nachos", "corn cups"],
        "American": ["trail mix", "yogurt parfait"],
        "Chinese": ["edamame", "egg drop soup"]
    }
}

# Build preferences list based on user selection
selected_meals = ["Breakfast", "Lunch", "Dinner", "Snacks"] if meal_type == "All Meals" else [meal_type]
preferences = []
for meal in selected_meals:
    preferences.extend(meal_options[meal].get(cuisine, meal_options[meal]["Any"]))

calories_per_meal = daily_calories / len(preferences)

# Function to get food data from USDA
def search_food(item):
    params = {
        "api_key": USDA_API_KEY,
        "query": item,
        "pageSize": 1
    }
    response = requests.get(USDA_SEARCH_URL, params=params)
    data = response.json()

    if data.get("foods"):
        food = data["foods"][0]
        nutrients = food.get("foodNutrients", [])
        nutrient_dict = {n["nutrientName"]: n["value"] for n in nutrients}
        return {
            "description": food["description"],
            "calories": nutrient_dict.get("Energy", 0),
            "protein": nutrient_dict.get("Protein", 0),
            "fat": nutrient_dict.get("Total lipid (fat)", 0),
            "carbs": nutrient_dict.get("Carbohydrate, by difference", 0)
        }
    else:
        return {"description": item, "calories": 0, "protein": 0, "fat": 0, "carbs": 0}

# Fetch meals and build dataframe
meal_data = []
for item in preferences:
    food_info = search_food(item)
    meal_data.append({
        "Meal": food_info["description"],
        "Target Calories": int(calories_per_meal),
        "Actual Calories": food_info["calories"],
        "Protein (g)": food_info["protein"],
        "Carbs (g)": food_info["carbs"],
        "Fat (g)": food_info["fat"]
    })

meal_df = pd.DataFrame(meal_data)
st.subheader("🥗 Personalized Meals")
st.dataframe(meal_df)

# Macro breakdown pie chart
st.subheader("🧬 Macro Breakdown")
total_macros = meal_df[["Protein (g)", "Carbs (g)", "Fat (g)"]].sum()

fig2, ax2 = plt.subplots()
ax2.pie(
    total_macros,
    labels=["Protein", "Carbs", "Fat"],
    autopct="%1.1f%%",
    startangle=90,
    colors=["#6FCF97", "#F2C94C", "#F2994A"]
)
ax2.axis("equal")
st.pyplot(fig2)
