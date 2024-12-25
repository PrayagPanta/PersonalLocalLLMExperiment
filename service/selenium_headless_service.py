from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


class HeadlessSeleniumService:
    def __init__(self):
        self.options = Options()
        self.options.headless = True  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def get_body_content(self, url):
        """Fetch the body HTML content of the specified URL."""
        self.driver.get(url)
        body_content = ""
        try:
            body_content = self.driver.find_element("tag name", "body").get_attribute('innerHTML')
        except Exception as e:
            logger.error(f"Cannot retreive html contents from {url} due to {e}")
        return body_content

    def close(self):
        """Close the browser and clean up."""
        self.driver.quit()


# if __name__ == "__main__":
#     # Example usage
#     service = HeadlessSeleniumService()
#
#     urls = [
#         "https://example.com",  # Replace with your target URLs
#         "https://www.wikipedia.org/",
#         # Add more URLs as needed
#     ]
#
#     for url in urls:
#         print(f"Fetching body content from: {url}")
#         body_content = service.get_body_content(url)
#         print(body_content[:500])  # Print the first 500 characters of the body content
#
#     service.close()
