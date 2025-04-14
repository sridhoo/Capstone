from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to interact with Ollama
def generate_meal_plan(user_input):
    ollama_url = "http://localhost:11434/api/generate"  # Ollama's local API endpoint
    payload = {
        "model": "mistral",  # Change if you're using a different model
        "prompt":  "",
        "quantize": "q4_K_M",
        "stream": False
    }
    response = requests.post(ollama_url, json=payload)
    return response.json()["response"]  # Extract the AI-generated meal plan

@app.route('/meal_plan', methods=['POST'])
def meal_plan():
    data = request.json
    user_input = data.get("preferences", "2000 calories, vegetarian")  # Default example
    meal_plan = generate_meal_plan(user_input)
    return jsonify({"meal_plan": meal_plan})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
