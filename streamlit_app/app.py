import streamlit as st
import requests

st.title("FitEats Meal Planner 🍽️")

# User input fields
diet_type = st.text_input("Enter your diet preferences (e.g., Vegan, 2000 calories)")
generate_btn = st.button("Generate Meal Plan")

if generate_btn:
    if diet_type:
        response = requests.post("http://localhost:5000/meal_plan", json={"preferences": diet_type})
        meal_plan = response.json()["meal_plan"]
        st.write("### Your Meal Plan")
        st.write(meal_plan)
    else:
        st.warning("Please enter your diet preferences!")
