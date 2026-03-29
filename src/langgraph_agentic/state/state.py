from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List, Optional


class State(TypedDict):
    messages: Annotated[List, add_messages]
    scraped_url: Optional[str]        # URL to scrape (Web Scraper Chatbot)
    scraped_content: Optional[str]    # Pre-fetched page content (cached per session)