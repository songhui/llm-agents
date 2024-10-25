from autogen import ConversableAgent, GroupChat
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import importlib.resources as resrc

import chromadb
import requests
from tools.neo4j import save_schema

def second_last_msg(sender: ConversableAgent, recipient: ConversableAgent, summary_args: dict):
    return sender.chat_messages[recipient][-2]["content"]

def describe_country(country_name:str)->str:
    #TODO: add description here too
    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="+country_name
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()  # Extract JSON content
        page = next(iter(json_data["query"]["pages"].values()))
        return page["extract"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def initialize(group_manager:ConversableAgent, first_agent:ConversableAgent, message:str, max_round:int=6):
    """
    Initialize the conversation between a group of agent.
    A group manager and the first agent to talk are needed. 
    A message must also be passed to provide the task or the question to answer.
    """
    first_agent.initiate_chat(group_manager, max_round= max_round, message= message)


#TODO: should be changed the way to rely on resrc lib
def retrieve_content(config:dict, file=resrc.files("llmagents") / "schema.json"):
    """
    """

    save_schema()
    if not file.is_file(): return None
    
    client = chromadb.PersistentClient(path=str(resrc.files("llmagents") / "tmp"))

    # Creates the new agent only if there is a schema
    return RetrieveUserProxyAgent(
        name="retriever",
        human_input_mode="NEVER",
        retrieve_config={
            "docs_path": str(file), # A list of urls, dirs or files can be passed
            "get_or_create": True,
            "extra_docs": True,
            "vector_db": client,
            "customized_prompt": "DATABASE SCHEMA\n{input_context}\n\nTASK\n{input_question}",
        },
        description="Assistant who has extra content retrieval power.")

def _reset_agents(group:GroupChat=None):
    if group:
        for a in group.agents: a.reset()