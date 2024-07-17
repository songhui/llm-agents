# llm-agents
A group of experiments using autogen

# Installation

We recommend to use jupyter notebook in docker

```bash 
git clone https://github.com/songhui/llm-agents
cd llm-agents
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work quay.io/jupyter/datascience-notebook:2024-05-27
```

After the container is running, open the notebook and navigate to the folder with the notebooks that you are interested in, e.g., "notebooks/summerschool". Remember to create a new 'openai.credential' file with your API token. 

In the folder, the libraries.ipynb file contains the pip commands to install some libraries used in the examples. Run this before playing with the sample notebooks, but only for the first time. 