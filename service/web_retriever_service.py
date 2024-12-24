from duckduckgo_search import DDGS
from service.ollama_query_service import OllamaQueryService
from loguru import logger


class WebRetriever:
    def __init__(self, search_engine_provider=DDGS(), llm_service=OllamaQueryService("llama3.1")):
        self.search_engine = search_engine_provider
        self.llm_service = llm_service

    def get_urls_for_topic(self, topic):
        return self.search_engine.text(topic, max_results=10)

    def get_summary_from_top_results(self,topic):
        urls_and_details_list = self.get_urls_for_topic(topic)
        logger.debug(f"Top 10 Url details list retrieved for {topic} were as following :: {urls_and_details_list}")
        top_urls = self.llm_service.rank_topic_and_get_top_urls(topic,urls_and_details_list)
        logger.info(f"Url list ranked by llm is as following :{top_urls}")
        get_summary_from_web_pages = self.llm_service.get_summary_from_top_urls(topic,top_urls[0:3])
        return get_summary_from_web_pages




search_engine_provider = WebRetriever()