import os

import google.generativeai as genai
from dotenv import load_dotenv

# API key call
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API key can't find")
    exit()

# Gemini API config
genai.configure(api_key=api_key)

# Agent create, Given system instruction with proper prompt
agent_instructions = """Your name is 'Cyber_Tech'. You are an expert with 15 years of experience in Cybersecurity and Networking.
You should only answer questions related to Networking, DevOps, cloud and Cybersecurity.
If someone asks about any other topic, please state very politely that you are not knowledgeable about that subject and that you can only assist with technical issues."""

# Buildup the model
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite", system_instruction=agent_instructions
)

# Start chat with agent
print(
    "🤖 Hello! I am Cyber_Tech. Ask your Networking and Security questions. (Type 'exit' to leave)"
)
print("-" * 50)

# Object for store the chat
chat = model.start_chat(history=[])

while True:
    user_input = input("\n 👤 You: ")

    if user_input.lower() == "exit":
        print("\n🤖 Cyber_Tech : Thank you! Good Bye...")
        break
    if not user_input.strip():
        continue

    try:
        # Get an answer from the agent
        response = chat.send_message(user_input)
        print(f"\n🤖 Cyber_Tech : {response.text}")
    except Exception as e:
        print(f"\n Error occur : {e}")
