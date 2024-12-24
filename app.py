from flask import Flask

from service.web_retriever_service import search_engine_provider
from loguru import  logger

app = Flask(__name__)

@app.route("/sample",methods=["GET"])
def get_sample_response():
    return "Sample Response"

@app.route("/web/summary/<topic>",methods=["GET"])
def get_detailed_response(topic):
    logger.info(f"Received summary request for {topic}")
    results = search_engine_provider.get_summary_from_top_results(topic)
    return results

if __name__ =="__main__":
    app.run(port=5000,debug=True)