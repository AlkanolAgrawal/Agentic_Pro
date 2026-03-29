import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json


class DisplayResults:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    # ──────────────────────────────────────────────────────────────────────
    # Simple ChatBot
    # ──────────────────────────────────────────────────────────────────────
    def display_basic_chatbot_results(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Simple ChatBot":
            with st.chat_message("user"):
                st.write(user_message)

            response = graph.stream(
                {"messages": ("user", user_message)}, stream_mode="values"
            )

            last_ai_message = None
            for event in response:
                last_ai_message = event

            with st.chat_message("assistant"):
                content = last_ai_message["messages"][-1].content
                # Strip chain-of-thought blocks (e.g., <think>…</think>)
                content = content.split("</think>")[-1].strip()
                st.write(content)

    # ──────────────────────────────────────────────────────────────────────
    # Web Scraper ChatBot
    # ──────────────────────────────────────────────────────────────────────
    def display_web_scraper_chatbot_results(self, scraped_url: str = "", scraped_content: str = ""):
        graph = self.graph
        user_message = self.user_message

        with st.chat_message("user"):
            st.write(user_message)

        if scraped_url:
            st.caption(f"🌐 Answering based on: [{scraped_url}]({scraped_url})")

        # Build initial state — content will be fetched inside the node if not cached
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "scraped_url": scraped_url,
            "scraped_content": scraped_content,
        }

        response_events = list(
            graph.stream(initial_state, stream_mode="values")
        )

        last_event = response_events[-1] if response_events else None

        if last_event:
            # Cache fetched content back to session so next message skips re-scrape
            if last_event.get("scraped_content"):
                st.session_state["scraped_content"] = last_event["scraped_content"]

            ai_msg = last_event["messages"][-1]
            content = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)
            content = content.split("</think>")[-1].strip()

            with st.chat_message("assistant"):
                st.write(content)
        else:
            st.error("No response received from the graph.")




            # response = graph.stream({"messages":("user",user_message)},stream_mode = "updates")##this will stream first human only message state 
            #     #and then new state with ai message along with human message
            # last = None
            # for x in response:
            #     last =  x
            # print(last)                                                                    //All this code is used if i use the method updates instead of values for streaming
            # with st.chat_message("assistant"):
            #     st.write(last["chatbot"]["messages"][0].content)  ##display only the last ai message content