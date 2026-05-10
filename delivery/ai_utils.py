from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = None

if api_key:
    client = Groq(api_key=api_key)


def recommend_food(mood, weather, taste, location="India"):

    if not client:
        return "Groq API key missing."

    prompt = f"""
    You are a professional AI food recommendation system.

    User Mood: {mood}
    Weather: {weather}
    Taste Preference: {taste}
    Location: {location}

    Recommend 5 foods.

    STRICT FORMAT:

    🍽 Food Name
    • Why this food matches mood/weather
    • Best place to eat
    • Ideal drink pairing

    Also suggest:
    - nearest famous restaurants
    - best cuisine
    - best dessert

    Keep response beautiful and structured.
    """

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"


def generate_recipe(dish):

    if not client:
        return "Groq API key missing."

    prompt = f"""
    Generate a professional recipe for:

    {dish}

    STRICT FORMAT:

    🍽 Dish Name

    ⏱ Cooking Time:
    🔥 Difficulty:
    🍴 Servings:
    🔥 Calories:

    🛒 Ingredients:
    - item 1
    - item 2

    👨‍🍳 Cooking Steps:
    1.
    2.
    3.

    💡 Chef Tips:
    - tip 1
    - tip 2

    Keep response clean and visually structured.
    """

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"