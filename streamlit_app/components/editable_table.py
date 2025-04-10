
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



