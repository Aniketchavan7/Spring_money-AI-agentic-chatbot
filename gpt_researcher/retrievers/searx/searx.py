import os
from langchain_community.utilities import SearxSearchWrapper

class SearxSearch:
    def __init__(self, query):
        self.query = query
        self.searx_url = self.get_searx_url()
        self.searx = SearxSearchWrapper(searx_host=self.searx_url)

    def get_searx_url(self):
        try:
            searx_url = os.environ["SEARX_URL"]
            if not searx_url:
                raise Exception("SEARX_URL environment variable is empty")
            return searx_url
        except KeyError:
            raise Exception("SEARX_URL environment variable not found")

    def search(self, max_results=7):
        try:
            results = self.searx.results(self.query, num_results=max_results)
            return [{"href": result["link"], "body": result["snippet"]} for result in results]
        except Exception as e:
            print(f"Error in Searx search: {e}")
            return []

