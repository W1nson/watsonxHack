# Hosting all the LLM setup for as the model for the agent

from langchain_ollama import ChatOllama
from langchain_ibm import ChatWatsonx
import os 
from dotenv import load_dotenv

load_dotenv()

WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Ollama LLM 
ollama_model = ChatOllama(model="granite3.3:latest")


# Watsonx LLM
watsonx_model = ChatWatsonx(
    model_id="ibm/granite-3-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=WATSONX_PROJECT_ID,
    api_key=WATSONX_APIKEY,
    params={"temperature": 0.7},
)


    

