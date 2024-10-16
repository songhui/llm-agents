# About the project
The project first usage was to experiments autogen. Those can be found in the `notebooks/summerschool` and `notebooks/test` directories. 
Recently was added a part to retrieve and review PSC papers and can be found in `notebooks/psc_expert` and `notebooks/literature`. 
To make reusable some functions between notebooks we created a `tools` directory where tools about papers, neo4j and agents management can be found. To make tools import available we used a dummy directory (`llmgents` with `__init__.py`) to package the project.

# Install the project

To clone this repository
```bash
git clone https://github.com/songhui/llm-agents
```

# Run in docker
WHile in the root directory launch:
```bash 
docker run -it --rm -v "${PWD}":/home/jovyan/work quay.io/jupyter/datascience-notebook:2024-05-27
```
This command will run jupyter cotainer only. To install dependencies you can run in a different terminal:
```bash
docekr exec <container_name> pip install poetry && poetry install  -C /home/jovyan/work
```


To launch both jupyter and neo4j you have to use:
```bash
docker-compose -f .devcontainer/docker-compose.yml up 
```
We decided to keep devcontainers the primary way of using this project, due to this decision you will have to install manually the required Python libraries.
In a different terminal you have to launch:
```bash
docekr exec notebook pip install poetry && poetry install -C /home/jovyan/project
```

After the container is running, open the notebook using the provided link by jupyter's container output and navigate to the folder with the notebooks that you are interested in, e.g., `notebooks/summerschool`. 
Remember to create a new `openai.credential` file in `notebook` directory with your API token. 
Remember to create/change the config_list for the LLM you want to use, `TEMPLATE_LIST` file will give you an inside on the type of information you should pass. 


# Alternative: run with devcontainers
If you installed the devcontainers extension in VScode, then simply open the workspace there. You will receive a prompt window asking if you want to reopen the workspace in container. Say yes, and you will be able run the notebooks in VS code. 
If this window does not pop up you can use the shortcut F1 and then search for 'Dev Containers: Open Folder in Container...', the folder to choose is the root directory of the project.