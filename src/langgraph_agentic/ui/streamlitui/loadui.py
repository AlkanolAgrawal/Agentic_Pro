import streamlit as st
import os

from src.langgraph_agentic.ui.uiconfig import UIConfig


class LoadStreamlitUI:
    def __init__(self):
        self.ui_config = UIConfig()
        self.user_controls = {}

    def load_streamlit_ui(self):
        title = self.ui_config.get_page_title()
        st.set_page_config(page_title=f"🤖 {title}", layout="wide")
        st.header(f"🤖 {title}")

        with st.sidebar:
            st.markdown("---")
            # ── LLM selection ──────────────────────────────────────────────
            llm_options = self.ui_config.get_llm_options()
            self.user_controls["llm_choice"] = st.selectbox("🧠 Select LLM Provider", llm_options)

            if self.user_controls["llm_choice"] == "Groq":
                groq_model_options = self.ui_config.get_groq_model_options()
                self.user_controls["groq_model_choice"] = st.selectbox(
                    "🔧 Select GROQ Model", groq_model_options
                )
                self.user_controls["GROQ_API_KEY"] = st.session_state[
                    "GROQ_API_KEY"
                ] = st.text_input(
                    "🔑 GROQ API Key", type="password", key="groq_api_key"
                )
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("GROQ API Key is required.")

            st.markdown("---")
            # ── Use-case selection ─────────────────────────────────────────
            usecase_options = self.ui_config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox(
                "🚀 Select Use Case", usecase_options
            )

            usecase = self.user_controls["selected_usecase"]

            # ── Web Scraper specific controls ──────────────────────────────
            if usecase == "Web Scraper ChatBot":
                st.markdown("#### 🌐 Web Scraper Settings")
                url_input = st.text_input(
                    "Enter URL to scrape",
                    placeholder="https://example.com",
                    key="scrape_url_input",
                )
                scrape_btn = st.button("🔍 Scrape URL", use_container_width=True)

                if scrape_btn and url_input:
                    # Clear cached content when user requests a new scrape
                    st.session_state["scraped_url"] = url_input
                    st.session_state["scraped_content"] = ""  # force re-scrape
                    st.success(f"URL queued for scraping: {url_input}")

                self.user_controls["scraped_url"] = st.session_state.get(
                    "scraped_url", ""
                )
                self.user_controls["scraped_content"] = st.session_state.get(
                    "scraped_content", ""
                )

                if not self.user_controls["scraped_url"]:
                    st.info("Enter a URL and click **Scrape URL** to begin.")

            # ── Super Chatbot Tavily key ───────────────────────────────────
            if usecase == "Super ChatBot(integrated with tools)":
                self.user_controls["TAVILY_API_KEY"] = st.session_state[
                    "TAVILY_API_KEY"
                ] = st.text_input(
                    "🔑 TAVILY API Key", type="password", key="tavily_api_key"
                )
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("TAVILY API Key is required for Super ChatBot.")

        return self.user_controls