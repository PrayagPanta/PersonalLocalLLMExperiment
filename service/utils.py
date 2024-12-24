import requests

def get_html_content_from_a_link(link:str)->str:
    html_text = requests.get(link).text
    return html_text