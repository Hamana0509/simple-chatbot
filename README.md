# Simple Chatbot with OpenAI Integration

# Overview

This project implements a simple chatbot that integrates OpenAI's GPT-4 model for conversational interactions, with a specific feature for weather retrieval using the OpenWeatherMap API. The chatbot can dynamically call the weather function when the user asks about the weather, either specifying a location or using a default location. Additionally, it handles basic conversation flows such as greetings and farewells.

# Key fearures

1. **Chatbot functionality**: The chatbot generates conversational responses using the OpenAI API. It creates a dynamic conversation by responding to the user's input.
2. **Weather Fetching**: The chatbot can retrieve current weather information using the OpenWeatherMap API for a given location, if user does not mention specific location then it will fetch weather data at user's predefined location.
3. **Function Calls**: The script demonstrates how to use OpenAI's function-calling capabilities to make external API requests during conversations.

# Requirements

- Python 3.x
- OpenAI API key
- OpenWeatherMap API key

## Libraries

- **OpenAI**: Interacts with the OpenAI GPT model to generate conversation responses.
- **Requests**: Fetches weather data from the OpenWeatherMap API.
- **JSON**: Handles the API request and response payloads in JSON format.
- **Instructor**: Instructor makes it easy to get structured data like JSON from LLMs like GPT-3.5, GPT-4, GPT-4-Vision, and open-source models.

## Reasons for choosing libraries or frameworks

1. OpenAI
   - The `openai` library is used to interact with OpenAI's GPT models, specifically the `GPT-4` model.
   - This library provides a seamless way to generate human-like conversational responses by leveraging state-of-the-art natural language processing models. Since the core functionality of the chatbot revolves around creating intelligent, context-aware conversations, `openai` is essential for generating dynamic responses.
   - OpenAI offers some of the most advanced models in the field of natural language understanding and generation. The `GPT-4` model is particularly well-suited for conversational applications due to its ability to handle multi-turn conversations, maintain context, and produce high-quality text output.
2. Requests
   - The `requests` library is used for making HTTP requests to external APIs, specifically the OpenWeatherMap API in this project.
   - The chatbot needs to fetch real-time weather information when the user asks for it. This is accomplished by sending requests to the OpenWeatherMap API, and `requests` is a simple and popular Python library for making HTTP calls.
   - `requests` is known for its simplicity and ease of use. It abstracts much of the complexity involved in sending HTTP requests and handling responses, making it an ideal choice for a project that needs to interact with external APIs efficiently.
3. JSON
   - The `json` module is used to parse and handle data in JSON format.
   - Both the OpenWeatherMap API and OpenAI API return data in JSON format. The `json` library allows you to easily decode and extract necessary information from these responses, such as weather descriptions and temperatures.
   - JSON is a lightweight and widely-used data format, especially in APIs. Python’s built-in `json` module is efficient for parsing and working with JSON data, so no additional libraries are required.

# Aproach

## Conversational Flow:

1. Conversational Flow:
   The chatbot initiates a friendly conversation, asks for the user’s name, and acknowledges it. It continuously accepts user input, determines whether the conversation should end based on certain phrases (e.g., "bye", "exit"), and responds accordingly.

2. OpenAI GPT-4 Integration:
   The chatbot uses OpenAI’s GPT-4 model to generate responses during the conversation. It utilizes the model's chat.completions.create method to generate conversational prompts, adhering to the system prompt that defines the chatbot’s behavior (e.g., being friendly and responsive).

   To improve user interaction, **function calling** is implemented to fetch real-time weather data. The model dynamically decides whether it needs to call the `get_current_weather` function based on user input.

3. Function Calling for Weather:
   When the user asks about the weather, the chatbot either:

   - Calls the `OpenWeatherMap` API for a location specified by the user.
   - Defaults to providing weather data for a predefined location, `Ho Chi Minh City, Vietnam`, if no location is specified.
     The chatbot retrieves and formats weather information, including temperature, humidity, and wind speed, then incorporates it into the conversation.

4. End of Conversation:
   A helper function, `determine_conversation_end`, analyzes user input for certain phrases to decide if the conversation should end. If such a phrase is detected, the chatbot generates a goodbye message and terminates the session.

# How to run

1. Clone this repository:

```python
git clone https://github.com/yourusername/simple-chatbot.git
```

2. Install the required libraries:

```python
pip install -r setup.txt
```

2. Update the API keys for `OpenAI` and `OpenWeatherMap` in the script:

```python
OPENAI_API_KEY = "your_openai_api_key"
WEATHER_API_KEY = "your_openweathermap_api_key"
```

3. Run the chatbot

```python
python simple_chatbot.py
```

# Reasoning Behind Choices

- **OpenAI GPT-4**: The GPT-4 model provides highly contextual and human-like responses, making it ideal for conversational agents like this chatbot. It also supports function calling, which allows the chatbot to trigger external APIs based on user input.

- **OpenWeatherMap API**: Chosen for its comprehensive weather data and ease of integration, OpenWeatherMap allows real-time weather information to be incorporated into the conversation.

- **Modular Design**: By separating concerns (conversation handling, weather API interaction, and function calling), the project is easier to maintain and extend.
