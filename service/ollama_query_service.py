import ast
import re
from concurrent.futures.thread import ThreadPoolExecutor
from http.client import HTTPException
from typing import List, Dict, Union

import html2text
from bs4 import BeautifulSoup

import requests
from loguru import logger

from config.config import jinja_env
from dataclass_dto.ollama_dataclasses import ModelRequest
#from service.selenium_headless_service import HeadlessSeleniumService


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
        #selenium_service = HeadlessSeleniumService()
        with ThreadPoolExecutor() as executor:
            html_contents = list(executor.map(self.get_html_page_content_from_url, top_urls))
        #selenium_service.close()
        summarize_prompt = (jinja_env.get_template("final_html_summarizer.txt")
        .render({"topic":topic,"html_list":html_contents}))
        logger.debug(f"Summarize prompt for topic : {topic} :: {summarize_prompt}")
        return self.query_ollama_model(summarize_prompt)

    def get_html_page_content_from_url(self, url):
        try:
            headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                       "accept-language": "en-US,en;q=0.9",
                       "cache-control": "max-age=0",
                       "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                    }
            html_response = requests.get(url,headers=headers)
            html_response.raise_for_status()
            #body = selenium_service.get_body_content(url)
            html_to_text = html2text.HTML2Text()
            html_to_text.ignore_images = True
            html_to_text.ignore_links = True
            html_to_text.ignore_emphasis = True
            body_text = html_to_text.handle(html_response.text).replace("\n"," ")
            return re.sub(r'\s{2,}', ' ', body_text)
            # soup = BeautifulSoup(html_response.text, 'html.parser')
            # body_text = soup.body.get_text(' | ', strip=True) if soup.body else ''
            #return body_text
        except Exception as e:
            logger.error(f"Error retrieving contents of URL {url} due to {e}")
            return ""




if __name__ == "__main__":
    llm_service = OllamaQueryService("llama3.1")
    html_content = llm_service.get_html_page_content_from_url( "https://pypi.org/project/pip/")
    print(html_content)







