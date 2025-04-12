import streamlit as st
import pandas as pd

def show_editable_meal_plan(plan_dict, key):
    try:
        data = []
        for day, meals in plan_dict.items():
            for meal_type in ["Breakfast", "Lunch", "Dinner"]:
                description = meals.get(meal_type, "No meal generated")
                if not isinstance(description, str):
                    description = str(description)
                data.append({
                    "Day": day,
                    "Meal Type": meal_type,
                    "Description": description
                })
        
        df = pd.DataFrame(data)
        
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
        
        st.write("Edit your meal plan below:")
        edited_df = st.data_editor(
            df,
            column_config=column_config,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key=key
        )
        
        with st.form(key=f"save_form_{key}"):
            submit = st.form_submit_button("💾 Save Changes")
            if submit:
                updated_plan = {}
                for _, row in edited_df.iterrows():
                    day = row["Day"]
                    meal_type = row["Meal Type"]
                    description = row["Description"]
                    
                    if day not in updated_plan:
                        updated_plan[day] = {}
                    updated_plan[day][meal_type] = description
                
                # Update session state and force re-render
                st.session_state["meal_plan"] = updated_plan
                st.success("✅ Changes saved! Meal plan updated.")
                st.rerun()  # Force Streamlit to re-render the page

    except Exception as e:
        st.error(f"🚨 Error in editable table: {e}")

