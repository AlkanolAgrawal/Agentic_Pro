from logging import exception
import streamlit as st
from src.langgraph_agentic.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraph_agentic.LLMs.groqllm import GroqLLM
from src.langgraph_agentic.graph.graph_builder import GraphBuilder
from src.langgraph_agentic.ui.streamlitui.display_results import DisplayResults


def load_langgraph_agentic_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.warning("Failed to load user input from UI.")
        return

    user_message = st.chat_input("Enter your message here...")
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_model()
            if not model:
                st.error("Failed to initialize the language model.")
                return

            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("No use case selected.")
                return

            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)

                display = DisplayResults(usecase, graph, user_message)

                if usecase == "Simple ChatBot":
                    display.display_basic_chatbot_results()

                elif usecase == "Web Scraper ChatBot":
                    scraped_url = user_input.get("scraped_url", "")
                    scraped_content = user_input.get("scraped_content", "")
                    if not scraped_url:
                        st.warning(
                            "⚠️ Please enter a URL in the sidebar and click **Scrape URL** first."
                        )
                    else:
                        display.display_web_scraper_chatbot_results(
                            scraped_url=scraped_url,
                            scraped_content=scraped_content,
                        )

                else:
                    st.info(f"Use case **{usecase}** is not yet wired up in this demo.")

            except Exception as e:
                st.error(f"Error setting up graph for use case '{usecase}': {e}")
                return

        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
