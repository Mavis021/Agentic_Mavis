from langchain_community.tools.tavily_search import TavilySearchResults
import os

from dotenv import load_dotenv

load_dotenv()

def get_profile_url_tavily(name: str):
    search = TavilySearchResults()
    res = search.run(f"{name}")

    return res


if __name__ == "__main__":
    name = "Mamata Maharjan"
    get_profile_url_tavily(name=name)