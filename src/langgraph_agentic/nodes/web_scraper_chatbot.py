import requests
from bs4 import BeautifulSoup
from langchain_core.messages import SystemMessage, HumanMessage


class WebScraperChatbot:
    """
    A chatbot node that scrapes a given URL and answers user questions
    about the scraped content using a Groq LLM.
    """

    def __init__(self, model):
        self.llm = model

    def _scrape_url(self, url: str) -> str:
        """Fetch and extract readable text from a URL."""
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script / style noise
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n")
            # Collapse blank lines and limit length to avoid token overflow
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned = "\n".join(lines)
            return cleaned[:12000]  # ~3k tokens
        except Exception as e:
            return f"⚠️ Failed to scrape URL: {e}"

    def process(self, state: dict) -> dict:
        """
        Expects state to contain:
            messages  — conversation history (standard LangGraph)
            scraped_url — the URL to scrape (optional; may be pre-scraped)
            scraped_content — already-scraped text (if available)
        """
        scraped_content = state.get("scraped_content", "")
        url = state.get("scraped_url", "")

        if not scraped_content and url:
            scraped_content = self._scrape_url(url)

        system_prompt = (
            "You are a helpful AI assistant. "
            "The user has provided the following web page content for you to analyse "
            "and answer questions about. "
            "If the content is empty or an error occurred, let the user know politely.\n\n"
            f"--- START OF SCRAPED CONTENT ---\n{scraped_content}\n--- END OF SCRAPED CONTENT ---"
        )

        messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
        response = self.llm.invoke(messages)

        return {
            "messages": [response],
            "scraped_content": scraped_content,
        }
