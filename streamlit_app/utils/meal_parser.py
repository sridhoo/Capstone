# import re

# def parse_meal_plan(raw_text, days):
#     plan = {}
#     current_day = None

#     for line in raw_text.splitlines():
#         line = line.strip()
#         if not line:
#             continue

#         day_match = re.match(r"(Day\s*\d+)", line, re.IGNORECASE)
#         meal_match = re.match(r"(Breakfast|Lunch|Dinner):", line, re.IGNORECASE)

#         if day_match:
#             current_day = day_match.group(1)
#             plan[current_day] = {}
#         elif meal_match and current_day:
#             meal_type = meal_match.group(1)
#             meal_desc = line.split(":", 1)[1].strip()
#             plan[current_day][meal_type] = meal_desc

#     # Fill in missing meals if necessary
#     for day in list(plan.keys())[:days]:
#         for meal in ["Breakfast", "Lunch", "Dinner"]:
#             plan[day].setdefault(meal, "")

#     return {k: plan[k] for k in list(plan)[:days]}

# import re

# def parse_meal_plan(raw_text, days):
#     plan = {}
#     current_day = None
    
#     # Split into days first
#     day_sections = re.split(r'(?i)(Day\s*\d+)', raw_text)
    
#     # The first element is empty if the text starts with Day
#     if day_sections and not day_sections[0]:
#         day_sections = day_sections[1:]
    
#     # Pair day headers with their content
#     for i in range(0, len(day_sections), 2):
#         if i+1 >= len(day_sections):
#             break
            
#         day_header = day_sections[i].strip()
#         day_content = day_sections[i+1]
        
#         if not day_header.lower().startswith('day'):
#             continue
            
#         day_meals = {}
#         for line in day_content.split('\n'):
#             line = line.strip()
#             if not line:
#                 continue
                
#             meal_match = re.match(r'(Breakfast|Lunch|Dinner):?\s*(.*)', line, re.IGNORECASE)
#             if meal_match:
#                 meal_type = meal_match.group(1).capitalize()
#                 meal_desc = meal_match.group(2).strip()
#                 day_meals[meal_type] = meal_desc
                
#         plan[day_header] = day_meals
    
#     # Ensure we have exactly the requested number of days
#     result = {}
#     for i in range(1, days+1):
#         day_key = f"Day {i}"
#         result[day_key] = plan.get(day_key, {
#             "Breakfast": "",
#             "Lunch": "",
#             "Dinner": ""
#         })
    
#     return result

import re

def parse_meal_plan(raw_text, days):
    """Improved parser that handles more formatting variations"""
    plan = {}
    
    # Normalize line endings and remove empty lines
    raw_text = '\n'.join(line.strip() for line in raw_text.splitlines() if line.strip())
    
    # Split into day sections more reliably
    day_sections = re.split(r'(?i)(^Day\s+\d+)', raw_text, flags=re.MULTILINE)
    
    # Remove empty elements
    day_sections = [section.strip() for section in day_sections if section.strip()]
    
    # Process each day section
    for i in range(0, len(day_sections), 2):
        if i+1 >= len(day_sections):
            break
            
        day_header = day_sections[i]
        day_content = day_sections[i+1]
        
        day_meals = {}
        current_meal = None
        
        for line in day_content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check for meal headers (more flexible matching)
            meal_match = re.match(r'^(Breakfast|Lunch|Dinner)[:\s]*(.*)', line, re.IGNORECASE)
            if meal_match:
                current_meal = meal_match.group(1).capitalize()
                meal_desc = meal_match.group(2).strip()
                if meal_desc:  # Only add if description exists
                    day_meals[current_meal] = meal_desc
            elif current_meal:  # Continuation of previous meal description
                day_meals[current_meal] += " " + line
                
        plan[day_header] = day_meals
    
    # Ensure we have exactly the requested number of days
    result = {}
    for i in range(1, days+1):
        day_key = f"Day {i}"
        result[day_key] = plan.get(day_key, {
            "Breakfast": "No meal generated",
            "Lunch": "No meal generated",
            "Dinner": "No meal generated"
        })
    
    return result