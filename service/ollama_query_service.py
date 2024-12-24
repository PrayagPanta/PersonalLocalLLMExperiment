import ast
from concurrent.futures.thread import ThreadPoolExecutor
from http.client import HTTPException
from typing import List, Dict, Union

import requests
from loguru import logger

from config.config import jinja_env
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
             raise HTTPException("Could not get proper response from the ollama API.")

    def rank_topic_and_get_top_urls(self,topic,url_and_details_dict:Dict)->List:
        ranking_prompt = (jinja_env.get_template("result_rank_prompt.txt")
                          .render({"topic":topic,"url_details_dict":url_and_details_dict}))
        return ast.literal_eval(self.query_ollama_model(ranking_prompt))


    def get_summary_from_top_urls(self,topic, top_urls):
        logger.info("Retrieving web pages for top 3 urls")
        with ThreadPoolExecutor() as executor:
            html_contents = list(executor.map(self.get_html_page_content, top_urls))
        summarize_prompt = (jinja_env.get_template("final_html_summarizer.txt")
        .render({"topic":topic,"html_list":html_contents}))
        return self.query_ollama_model(summarize_prompt)

    def get_html_page_content(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error("Error retrieving URL %s: %s", url, e)
            return ""













