# llm-agents
A group of experiments using autogen

# Installation

We recommend to use jupyter notebook in docker

```bash 
git clone https://github.com/songhui/llm-agents
cd llm-agents
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work quay.io/jupyter/datascience-notebook:2024-05-27
```

After the container is running, open the notebook and navigate to the notebooks. Remember to create a new 'openai.credential' file with your API tokens. 