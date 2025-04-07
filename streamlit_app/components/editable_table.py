# components/editable_table.py
# import streamlit as st
# import pandas as pd

# def show_editable_meal_plan(default_meals=None):
#     st.markdown("## 🛠️ Customize Your Meal Plan")

#     # Default data (can be replaced with parsed AI output later)
#     data = default_meals or {
#         "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
#         "Food Item": ["Oatmeal", "Grilled Chicken Salad", "Stir-fry Veggies", "Greek Yogurt"],
#         "Calories": [300, 500, 400, 150],
#         "Protein (g)": [10, 35, 15, 12],
#         "Carbs (g)": [45, 30, 40, 10],
#         "Fat (g)": [5, 15, 10, 5]
#     }

#     df = pd.DataFrame(data)

#     edited_df = st.data_editor(
#         df,
#         num_rows="dynamic",
#         use_container_width=True,
#         key="diet_table",
#         column_config={
#             "Meal": st.column_config.SelectboxColumn("Meal", options=["Breakfast", "Lunch", "Dinner", "Snack"]),
#             "Calories": st.column_config.NumberColumn("Calories", step=50, min_value=0),
#             "Protein (g)": st.column_config.NumberColumn("Protein (g)", step=5),
#             "Carbs (g)": st.column_config.NumberColumn("Carbs (g)", step=5),
#             "Fat (g)": st.column_config.NumberColumn("Fat (g)", step=5),
#         }
#     )

#     if st.button("💾 Save Meal Plan"):
#         st.success("✅ Meal Plan Saved!")
#         st.dataframe(edited_df)

#     return edited_df

# import streamlit as st
# import pandas as pd

# def show_editable_meal_plan():
#     # Sample structured meal plan
#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     meals = ["Breakfast", "Lunch", "Dinner"]

#     structured_meal_plan = []
#     for day in days:
#         for meal in meals:
#             structured_meal_plan.append({
#                 "Day": day,
#                 "Meal Type": meal,
#                 "Food": f"Sample {meal} for {day}",
#                 "Calories": 400,
#                 "Protein (g)": 25,
#                 "Carbs (g)": 45,
#                 "Fats (g)": 15
#             })

#     df = pd.DataFrame(structured_meal_plan)

#     st.markdown("### ✍️ Edit Your Weekly Meal Plan")
#     edited_df = st.data_editor(
#         df,
#         column_config={
#             "Day": st.column_config.TextColumn(disabled=True),
#             "Meal Type": st.column_config.TextColumn(disabled=True),
#             "Food": st.column_config.TextColumn(),
#             "Calories": st.column_config.NumberColumn(),
#             "Protein (g)": st.column_config.NumberColumn(),
#             "Carbs (g)": st.column_config.NumberColumn(),
#             "Fats (g)": st.column_config.NumberColumn()
#         },
#         use_container_width=True,
#         key="editable_meal_plan"
#     )

#     st.success("✅ Changes will be saved during this session.")
#     return edited_df

# import streamlit as st
# import pandas as pd

# def show_editable_meal_plan(plan_dict):
#     rows = []
#     for day, meals in plan_dict.items():
#         for meal, desc in meals.items():
#             rows.append({"Day": day, "Meal": meal, "Description": desc})

#     df = pd.DataFrame(rows)

#     edited_df = st.data_editor(
#         df,
#         use_container_width=True,
#         hide_index=True,
#         key="editable_table"
#     )

#     if st.button("💾 Save Changes"):
#         st.session_state["updated_plan"] = edited_df
#         st.success("✅ Changes saved!")

# UPDATED
import streamlit as st
import pandas as pd

def show_editable_meal_plan(plan_dict):
    # Convert to DataFrame with better structure
    data = []
    for day, meals in plan_dict.items():
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            data.append({
                "Day": day,
                "Meal Type": meal_type,
                "Description": meals.get(meal_type, "No meal generated")
            })
    
    df = pd.DataFrame(data)
    
    # Configure columns for better editing
    column_config = {
        "Day": st.column_config.TextColumn("Day", disabled=True),
        "Meal Type": st.column_config.SelectboxColumn(
            "Meal Type",
            options=["Breakfast", "Lunch", "Dinner"],
            required=True
        ),
        "Description": st.column_config.TextColumn(
            "Description",
            width="large",
            required=True
        )
    }
    
    # Display the editable table
    st.write("Edit your meal plan below:")
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="meal_plan_editor"
    )
    
    # Save changes button
    if st.button("💾 Save Changes", key="save_changes_button"):
        # Convert back to the original structure
        updated_plan = {}
        for _, row in edited_df.iterrows():
            day = row["Day"]
            meal_type = row["Meal Type"]
            description = row["Description"]
            
            if day not in updated_plan:
                updated_plan[day] = {}
            updated_plan[day][meal_type] = description
        
        st.session_state["updated_plan"] = updated_plan
        st.success("✅ Changes saved!")
        
        # Show the updated plan in a nicer format
        st.subheader("📋 Updated Meal Plan")
        for day, meals in updated_plan.items():
            with st.expander(f"📅 {day}"):
                cols = st.columns(3)
                for i, (meal, desc) in enumerate(meals.items()):
                    cols[i].markdown(f"**{meal}**")
                    cols[i].write(desc)

