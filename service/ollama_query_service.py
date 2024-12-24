from http.client import HTTPException
from typing import List, Dict, Union

import requests
import json
from jinja2 import Environment, FileSystemLoader

from dataclass_dto.ollama_dataclasses import ModelRequest


class OllamaQueryService():
    def __init__(self,model_name,url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.url = url

    def query_ollama_model(self,query:str)->Union[str,List]:
        request_body = ModelRequest(self.model_name,query,False).__dict__
        model_response = requests.post(url=self.url,json=request_body)
        if model_response.status_code == 200:
            return model_response.json().get("response","")
        else:
             raise HTTPException("Could not get proper response from the ollama API. ")

    def rank_topic_and_get_top_urls(self,topic,url_and_details_dict:Dict)->List:
        jinja_env = Environment(loader=FileSystemLoader("/home/prayag/PycharmProjects/PythonProject1/service/prompts/"))
        ranking_prompt = (jinja_env.get_template("result_rank_prompt.txt")
                          .render({"topic":topic,"url_details_dict":url_and_details_dict}))
        return self.query_ollama_model(ranking_prompt)







