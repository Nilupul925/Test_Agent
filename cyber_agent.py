import os
import socket
import sys

import google.generativeai as genai
from dotenv import load_dotenv

# API key call
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API key can't find")
    sys.exit()

# Gemini API config
genai.configure(api_key=api_key)


# Custom function for domain check
def run_port_scanner(target_ip_or_domain: str) -> str:
    """
    It checks the open ports on the provided target IP address and domain.
    """
    print(f"\n[🔧 AI Tool active: Scanning {target_ip_or_domain}, Please wait...]")

    # Scanning ports
    ports_to_scan = [21, 22, 80, 443, 8080, 3306]
    open_ports = []

    try:
        # convert domain name into it's IP address
        target_ip = socket.gethostbyname(target_ip_or_domain)
    except socket.gaierror:
        return f"Error: Can't convet {target_ip_or_domain} into an IP address."

    # Chech each port
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # for speedly time out
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            open_ports.append(str(port))

        sock.close()

    # Pass result to Agent
    if open_ports:
        return f"Scan successful. Open ports on {target_ip_or_domain} ({target_ip}) : {','.join(open_ports)}"
    else:
        return f"Scan complete. None of the ports checked on {target_ip_or_domain} ({target_ip}) are open."


# Agent create, Given system instruction with proper prompt
agent_instructions = """Your name is 'Cyber_Tech'. You are an expert with 15 years of experience in Cybersecurity and Networking.
You should only answer questions related to Networking, DevOps, cloud and Cybersecurity.
If someone asks about any other topic, please state very politely that you are not knowledgeable about that subject and that you can only assist with technical issues.
If you are asked to check (scan) the status of a website or an IP address, or to examine its ports, you must use the provided 'run_port_scanner' tool to obtain the actual information.
please ensuring your response is clear and professional."""

# Buildup the model
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    system_instruction=agent_instructions,
    tools=[run_port_scanner],
)

# Start chat with agent
print(
    "🤖 Hello! I am Cyber_Tech. Ask your Networking and Security questions. (Type 'exit' to leave)"
)
print("-" * 50)

# Object for store the chat
# Enable automatic function calling
chat = model.start_chat(enable_automatic_function_calling=True, history=[])

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
