from autogen import ConversableAgent
import requests

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