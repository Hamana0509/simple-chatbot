import json
import os

import instructor
import reques
from openai import OpenAI

OPENAI_API_KEY = "YOUR OPENAI API KEY"
WEATHER_API_KEY = "YOUR WEATHER API KEY"
CURRENT_LOCATION = "Ho Chi Minh City, Vietnam"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["WEATHER_API_KEY"] = WEATHER_API_KEY

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = instructor.patch(client)


def get_llm_response(history=None, text=None, functions=None):
    if text is not None:
        prompt = [{"role": "system", "content": text}]
        messages = history + prompt
    else:
        messages = history

    # Create llm response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.8,
        max_tokens=256,
        top_p=1,
        functions=functions if functions is not None else None,
        function_call="auto" if functions is not None else None,
    )
    return response.choices[0].message


def get_current_weather(location=None):
    """
    Fetches current weather data for a given location from OpenWeatherMap API.
    Args:
        location (str): The location for which to get the weather.
    Returns:
        json: A json describing the current weather in location.
    """
    location = CURRENT_LOCATION if location is None else location
    # Make a request to the OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": os.getenv("WEATHER_API_KEY"), "units": "metric"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant data
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        # Create Json describing the current weather in location
        response_json = {
            "location": str(location),
            "description": str(weather_description),
            "temperature": str(temperature) + "°C",
            "humidity": str(humidity) + "%",
            "wind_speed": str(wind_speed) + "m/s",
        }
        return json.dumps(response_json)
    else:
        return f"Sorry, I couldn't find weather data for '{location}'. Please make sure the city name is spelled correctly."


def chat_with_llm(message_input):
    messages = [
        {
            "role": "system",
            "content": "Base on the information return by function calling to answer question.",
        },
        {"role": "user", "content": message_input},
    ]

    # Define the function that can be called by the model
    functions = [
        {
            "name": "get_current_weather",
            "description": (
                f"Get the current weather. If the location is not provided, use the default location '{CURRENT_LOCATION}'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country, e.g., 'Ho Chi Minh City, Vietnam', 'New York, USA', 'Tokyo, Japan'",
                    }
                },
                "required": ["location"],
            },
        }
    ]

    # Call the OpenAI ChatCompletion API with function calling
    # Get the assistant's message
    response = get_llm_response(messages, None, functions)

    if response.function_call:
        function_call = response.function_call
        function_name = function_call.name
        function_args = json.loads(function_call.arguments)
        if function_name == "get_current_weather":
            location = function_args.get("location")
            # Call the actual function
            weather_info = get_current_weather(location)
            # Add the function's response to the history
            messages.append(
                {"role": "function", "name": function_name, "content": weather_info}
            )
            # The assistant uses the function's response to generate a reply
            response = get_llm_response(messages, None)
            return response.content
    else:
        # If no function is called, the assistant uses the model's response
        return response.content


def determine_conversation_end(user_input):
    # Determine if the user wants to end the conversation contextually
    # We will consider intent and keywords in a sentence structure.
    goodbye_phrases = ["bye", "goodbye", "see you", "exit", "quit"]
    # Check if any farewell phrases are used with end intentions
    if any(phrase in user_input for phrase in goodbye_phrases):
        return True
    return False


def chatbot():
    history = []

    # Predefine prompt for model if user does not provide specific location when asking about weather
    system_prompt = (
        "You are a friendly chatbot. If the user asks about the weather and does not specify a location, "
        f"you should provide the weather for '{CURRENT_LOCATION}' without asking the user for their location."
    )
    history.append({"role": "system", "content": system_prompt})

    # Step 1: Generate greeting and ask for user's name using the model
    greeting_prompt = (
        "You are a friendly chatbot. Greet the user and ask for their name."
    )
    response = get_llm_response(history, greeting_prompt).content
    print(f"Chatbot: {response}")
    history.append({"role": "assistant", "content": response})

    # Step 2: Get the user's name
    user_name = input("You: ")
    history.append({"role": "user", "content": user_name})
    # Acknowledge the user's name dynamically
    acknowledge_prompt = f"You are a friendly chatbot. The user's name is {user_name}. Acknowledge their name and continue the conversation."
    response = get_llm_response(
        history, acknowledge_prompt
    ).content  # Use the acknowledge prompt here
    print(f"Chatbot: {response}")
    history.append({"role": "assistant", "content": response})

    while True:
        user_input = input("You: ")
        history.append({"role": "user", "content": user_input})

        # Recognize end of conversation commands
        if determine_conversation_end(user_input.lower()):
            # Generate goodbye message using the model
            goodbye_prompt = f"You are a friendly chatbot. The user's name is {user_name}. The user said '{user_input}'. Respond with a goodbye message."
            goodbye_message = get_llm_response(history, goodbye_prompt).content
            print(f"Chatbot: {goodbye_message}")
            history.append({"role": "assistant", "content": goodbye_message})
            break
        else:
            response = chat_with_llm(user_input)
            print(f"Chatbot: {response}")
            history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    chatbot()
