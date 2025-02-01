from duckduckgo_search import DDGS

class Duckduckgo:
    def __init__(self, query):
        self.query = query
        self.ddg = DDGS()

    def search(self, max_results=7):
        try:
            results = []
            for r in self.ddg.text(self.query, region='wt-wt', max_results=max_results):
                results.append({
                    "href": r["link"],
                    "body": r["body"]
                })
            return results
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            return []


