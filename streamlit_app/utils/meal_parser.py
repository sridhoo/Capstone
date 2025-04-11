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
