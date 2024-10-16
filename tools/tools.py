from autogen import ConversableAgent
import requests

def second_last_msg(sender: ConversableAgent, recipient: ConversableAgent, summary_args: dict):
    return sender.chat_messages[recipient][-2]["content"]

def describe_country(country_name:str)->str:
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


####TODO: SHOULD BE THE SAME INITIALIZE() BUT WITH CUSTOM MESSAGES!!!
def initialize(group_manager:ConversableAgent, first_agent:ConversableAgent):

    first_agent.initiate_chat(
        group_manager,
        max_round = 6,
        message = "Let's start with paper 10.1126/scitranslmed.abb3107. Please get its title and abstract. After that, save the following review to the existing paper with DOI 10.1126/scitranslmed.abb3107: Xiaojun has reviewed the paper (DOI: 10.1126/scitranslmed.abb3107) and judges that is a paper about PSC, and she commented that it is one of the primary work in this field. For this paper, no need to ask an additional opinion on whether it is about PSC or not."
    )

def expand_references(group_manager:ConversableAgent, first_agent:ConversableAgent):
    first_agent.initiate_chat(
        group_manager,
        max_round = 6,
        message = "Your task is as follows: "
            "1. Please query from the notes (the knowledge graph) to find one paper"
            "which has been Reviewed as YES for PSC research, and get its DOI."
            "2. If you find such as paper, retrieve all its citations, as a list of DOIs."
            "3. For each DOI in the citation list, create a Paper node in the knowledge graph, "
            "with only the property of DOI, and create a 'Cites' relation from the original paper (matched by its DOI) to the newly created paper. "
            "Since there will normally be many citations, "
            "please use a batch of data and the UNWIND keyword to create/merge these nodes in one cypher query."
    )

def review_paper(group_manager:ConversableAgent, first_agent:ConversableAgent):
    first_agent.initiate_chat(
        group_manager,
        max_round = 6,
        message = "Your task is as follows: "
            "1. Query your note (the graph) to find one paper which has not been reviewed. Done for the graph tool."
            "2. Use another tool to retrieve the title and abstract of this paper, and save the details into the graph."
            "3. Ask the psc_checker to see if it is about psc"
            "4. Save the Review about this paper, with YES/NO and comment, and record that this review is done by generative AI"
    )

