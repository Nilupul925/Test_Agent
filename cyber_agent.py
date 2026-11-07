import os
import socket

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Page config
st.set_page_config(
    page_title="Cyber_Tech AI Dashboard", page_icon="🛡️", layout="centered"
)
st.title("🌐 Cyber_Tech - AI Security Agent")
st.caption(
    "Your AI assistant for resolving Cybersecurity and Networking issues, and for performing port scans."
)
st.divider()

# API key call
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Error: API key can't find")
    st.stop()

# Gemini API config
genai.configure(api_key=api_key)


# Custom function for domain check
def run_port_scanner(target_ip_or_domain: str) -> str:
    """
    It checks the open ports on the provided target IP address and domain.
    """

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

# AI chat object
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        enable_automatic_function_calling=True
    )
# list of chats that show in UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old chat in UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting user input and reply
if user_prompt := st.chat_input("Submit an IP-related or technical issue."):
    # Show user input on UI and store them
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Assistant's reply with loading animation
    with st.chat_message("assistant"):
        with st.spinner("Cyber_Tech is thinking/ scanning... 🔍"):
            try:
                response = st.session_state.chat_session.send_message(user_prompt)
                st.markdown(response.text)

                # add the memory of assistant
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error occur: {e}")
