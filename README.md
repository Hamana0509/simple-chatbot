# Simple Chatbot with Weather Functionality

# Overview

This Python-based chatbot script uses the OpenAI GPT-3.5-turbo model to engage in simple conversation with the user, incorporating real-time weather information using the OpenWeatherMap API. The chatbot can greet the user, take input, and respond accordingly, while also calling external APIs to fetch current weather information based on user queries.

# Key fearures

1. **Chatbot functionality**: The chatbot generates conversational responses using the OpenAI API. It creates a dynamic conversation by responding to the user's input.
2. **Weather Fetching**: The chatbot can retrieve current weather information for a given location using the OpenWeatherMap API.
3. **Function Calls**: The script demonstrates how to use OpenAI's function-calling capabilities to make external API requests during conversations.

# Requirements

- Python 3.x
- OpenAI API key
- OpenWeatherMap API key

## Libraries

**OpenAI**: Interacts with the OpenAI GPT model to generate conversation responses.
**Requests**: Fetches weather data from the OpenWeatherMap API.
**JSON**: Handles the API request and response payloads in JSON format.

## Reasons for choosing libraries or frameworks

1. OpenAI
   - The `openai` library is used to interact with OpenAI's GPT models, specifically the `GPT-3.5-turbo` model.
   - This library provides a seamless way to generate human-like conversational responses by leveraging state-of-the-art natural language processing models. Since the core functionality of the chatbot revolves around creating intelligent, context-aware conversations, `openai` is essential for generating dynamic responses.
   - OpenAI offers some of the most advanced models in the field of natural language understanding and generation. The `GPT-3.5-turbo` model is particularly well-suited for conversational applications due to its ability to handle multi-turn conversations, maintain context, and produce high-quality text output.
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

1. The chatbot starts by greeting the user and asking for their name.
2. User inputs are appended to the conversation history, which is then passed to OpenAI's `gpt-3.5-turbo model` to generate appropriate responses.
3. The chatbot manages a simple conversation loop, printing both user inputs and bot responses.

## Weather Retrieval:

1. When a user asks about the weather, the chatbot calls the `get_current_weather()` function.
2. This function uses the OpenWeatherMap API to fetch the current weather information for the specified location.
3. The result is then returned to the chatbot and presented in the conversation.

# How to run

1. Install the required libraries:

```python
pip install -r setup.txt
```

2. Update the API keys for OpenAI and OpenWeatherMap in the script:

```python
OPENAI_API_KEY = "your_openai_api_key"
WEATHER_API_KEY = "your_openweathermap_api_key"
```

3. Run the chatbot

```python
python simple_chatbot.py
```
