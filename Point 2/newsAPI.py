from newsapi import NewsApiClient
import os
import autogen

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API"))

all_articles = newsapi.get_everything(q='Basketball', language="en"
                                     )
article = ""
for i in all_articles["articles"]:
    if i != None:
        article += i["content"]
gemini_api_key = os.getenv("API_KEY")
llm_config = {
  "model": "gemini-1.5-flash-latest",
  "api_key": gemini_api_key,
  "api_type": "google"
}

task = "write an article summarizing all the retrieved information from the latest news about basketball"

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="Give the task, and send instructions to writer to refine article.",
    code_execution_config=False,
    llm_config=llm_config,
    human_input_mode="ALWAYS",
)
planner = autogen.ConversableAgent(
    name="Planner",
    system_message="Given a task, please determine "
    "what information is needed to complete the task. "
    "Please note that the all the stock information will be retrieved using the researcher. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps. If a step fails, try to workaround",
    description="Planner. Given a task, determine what "
    "information is needed to complete the task. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps",
    llm_config=llm_config,
)
writer = autogen.ConversableAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Writer."
    "Please write articles in markdown format (with relevant titles)"
    " and put the content in pseudo ```md``` code block. "
    "You take feedback from the admin and refine your blog."
    "The information you have to use is this: " + article,
    description="Writer."
    "Write blogs based on the given information and take "
    "feedback from the admin to refine the article."
)
critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive "
                "feedback to help improve the quality of the content.",
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, critic , writer, planner],
    messages=[],
    max_round=10,
    allowed_or_disallowed_speaker_transitions={
        user_proxy: [critic, writer, planner],
        writer: [planner],
        planner: [user_proxy, critic, writer],
    },
    speaker_transitions_type="allowed",
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config=llm_config
)

groupchat_result = user_proxy.initiate_chat(
    manager,
    message=task,
)
