import os
from dotenv import load_dotenv, find_dotenv
from autogen import ConversableAgent

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("API_KEY")
llm_config = { "model": "gemini-1.5-flash-latest", "api_key": gemini_api_key, "api_type": "google" }


cathy = ConversableAgent(
    name="cathy",
    system_message="Your name is Cathy and you are a stand-up comedian.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "Start the next joke from the punchline of the previous joke.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe. Cathy, let's keep the jokes rolling.",
    max_turns=2,
)

cathy.send(message="What's last joke we said?", recipient=joe, request_reply=True)
