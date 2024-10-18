import json
import os

import regex as re
import requests
from openai import OpenAI

OPENAI_API_KEY = "your OpenAI API key"
WEATHER_API_KEY = "your openweathermap API key"


client = OpenAI(
    api_key="your OpenAI API key",
)


def get_current_weather(location):
    """
    Fetches current weather data for a given location from OpenWeatherMap API.

    Args:
        location (str): The location for which to get the weather.

    Returns:
        str: A string describing the current weather.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant data
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        # Build a response string
        weather_info = f"The current weather in {location} is {weather_description} with a temperature of {temperature}°C."
        return weather_info
    else:
        return f"Sorry, I couldn't find weather data for '{location}'. Please make sure the city name is spelled correctly."


def create_response(conversation, text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation + [{"role": "system", "content": text}],
        temperature=0.7,
        max_tokens=256,
    )
    return response.choices[0].message.content


def chatbot():
    conversation = []

    # Step 1: Generate greeting and ask for user's name using the model
    greeting_prompt = (
        "You are a friendly chatbot. Greet the user and ask for their name."
    )
    greeting_message = create_response(conversation, greeting_prompt)
    print(f"Chatbot: {greeting_message}")
    conversation.append({"role": "assistant", "content": greeting_message})

    # Step 2: Get the user's name
    user_name = input("You: ")
    conversation.append({"role": "user", "content": user_name})

    # Acknowledge the user's name dynamically
    acknowledge_prompt = f"You are a friendly chatbot. The user's name is {user_name}. Acknowledge their name and continue the conversation."
    acknowledge_message = create_response(
        conversation, acknowledge_prompt
    )  # Use the acknowledge prompt here
    print(f"Chatbot: {acknowledge_message}")
    conversation.append({"role": "assistant", "content": acknowledge_message})

    # Step 3: Enter chat loop
    while True:
        user_input = input("You: ")
        conversation.append({"role": "user", "content": user_input})

        # Recognize end of conversation commands
        if user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
            # Generate goodbye message using the model
            goodbye_prompt = f"You are a friendly chatbot. The user's name is {user_name}. The user said '{user_input}'. Respond with a goodbye message."
            goodbye_message = create_response(conversation, goodbye_prompt)
            print(f"Chatbot: {goodbye_message}")
            conversation.append({"role": "assistant", "content": goodbye_message})
            break

        # Define the function that can be called by the model
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Model that supports function calling
            messages=conversation,
            functions=functions,
            function_call="auto",  # Auto mode; the model decides whether to call a function
        )

        # Get the assistant's message
        message = response.choices[0].message

        if message.function_call:
            # The model wants to call a function
            function_call = message.function_call
            function_name = function_call.name  # Access 'name' using dot notation
            arguments = function_call.arguments  # Access 'arguments' using dot notation
            # Parse the arguments as JSON
            try:
                args = json.loads(arguments)
            except json.JSONDecodeError:
                args = {}

            if function_name == "get_current_weather":
                location = args.get("location")
                # Call the actual function
                weather_info = get_current_weather(location)
                # Add the function's response to the conversation
                conversation.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": weather_info,
                    }
                )
                # The assistant uses the function's response to generate a reply
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=conversation,
                    temperature=0.7,
                    max_tokens=256,
                )
                message = response.choices[0].message
                print(f"Chatbot: {message.content}")
                conversation.append({"role": "assistant", "content": message.content})
            else:
                # The assistant responds normally
                print(
                    f"Chatbot: {message.content}"
                )  # Changed line to access content correctly
                conversation.append(
                    {"role": "assistant", "content": message.content}
                )  # Changed line to access content correctly

        else:
            # The assistant responds normally
            print(f"Chatbot: {message.content}")
            conversation.append({"role": "assistant", "content": message.content})


if __name__ == "__main__":
    chatbot()
