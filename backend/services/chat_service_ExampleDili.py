from dotenv import load_dotenv # adds .env variables to project
import os
import openai

# Load .env file
load_dotenv()

# Openai API client and authentication
key = os.environ['API_KEY'] # Store api key in a variable
client = openai.OpenAI(api_key=key)

# Modify system prompt by changing the value for content here
conversation_history = [
    {
        "role":"system", "content":
        "You are a helpful assistant"
    }
]

# Define function to interact with ChatGPT API, Takes in a message string and generates a response
def chat_with_gpt(user_input):
    """Sends a message to ChatGPT and returns the response."""
    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4o-mini model
        messages=conversation_history,
        temperature=0.7,  # Adjust for more creative responses
        max_tokens=100
    )

    # Extract response text
    chatbot_reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": chatbot_reply})
    return conversation_history
