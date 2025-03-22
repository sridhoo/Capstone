import openai

OPENAI_API_KEY = "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"

def get_meal_plan(diet, goal, restrictions):
    prompt = f"""
    Create a 7-day meal plan for someone who follows a {diet} diet, aims to {goal}, and has the following dietary restrictions: {restrictions}.
    Include breakfast, lunch, dinner, and snacks for each day.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Correct way to initialize OpenAI client

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content  # Correct way to access response content

# Get user input
diet = input("What type of diet do you follow? (e.g., vegetarian, keto, etc.): ")
goal = input("What is your goal? (e.g., weight loss, muscle gain, maintenance): ")
restrictions = input("Any dietary restrictions? (e.g., no dairy, gluten-free): ")

# Generate meal plan
print("\nGenerating your meal plan...\n")
meal_plan = get_meal_plan(diet, goal, restrictions)
print(meal_plan)