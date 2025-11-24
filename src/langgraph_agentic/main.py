import streamlit as st 
from src.langgraph_agentic.ui.streamlitui.loadui import LoadStreamlitUI

def load_langgraph_agentic_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.warning("Failed to load user input from UI.")
        return
    user_message = st.chat_input("Enter your message here...")