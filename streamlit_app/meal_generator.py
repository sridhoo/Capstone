import subprocess

def generate_meal_plan_with_ollama(user_input, days=3):
    prompt = f"""
    Create a {days}-day personalized meal plan based on the following information: "{user_input}".
    Each day should include:
    - Breakfast
    - Lunch
    - Dinner

    Format it exactly like this:
    Day 1:
    - Breakfast: ...
    - Lunch: ...
    - Dinner: ...

    Day 2:
    - Breakfast: ...
    - Lunch: ...
    - Dinner: ...

    Keep the output clear and human-readable.
    """

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = result.stdout.strip()
    
    # Safety net: handle blank or short responses
    if not output or len(output.splitlines()) < 3:
        return "⚠️ Meal plan could not be generated. Please try again or check your model setup."
    
    return output
