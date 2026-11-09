import logging #To log warnings when DuckDuckGo or Wikipedia lookups fail
from ddgs.exceptions import DDGSException
from langchain.tools import tool  # To create a tool that can be used by the agent to search for info
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from requests.exceptions import RequestException
from wikipedia.exceptions import WikipediaException

logger = logging.getLogger(__name__)

search = DuckDuckGoSearchRun(
    api_wrapper=DuckDuckGoSearchAPIWrapper(region="us-en")
)

@tool(
    "search",
    description="Search the web for information when you need an answer to something you are not really aware of."
)
def search_tool(query: str) -> str:
    try:
        return search.run(query)
    except DDGSException as error:
        logger.warning("DuckDuckGo search failed; continuing without it: %s", error)
        return (
            "Web search failed and returned no results. Do not invent sources or "
            "claim this answer was verified online. Give a cautious answer based "
            "on existing knowledge and state that live sources could not be checked."
        )

api_wrapper2 = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_count=100)


@tool(
    "wikipedia_search",
    description="Search Wikipedia for background information about a rumor or claim.",
)
def tool_for_wiki(query: str) -> str:
    try:
        return api_wrapper2.run(query)
    except (RequestException, WikipediaException) as error:
        logger.warning("Wikipedia lookup failed; continuing without it: %s", error)
        return (
            "Wikipedia lookup failed because its service returned an invalid response "
            "or could not be reached. Do not treat Wikipedia as a source for this "
            "answer; continue with other available sources and be transparent if "
            "the claim could not be verified."
        )