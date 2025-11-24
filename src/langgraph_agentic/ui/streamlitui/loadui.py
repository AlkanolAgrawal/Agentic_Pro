import streamlit as st 
import os 

from src.langgraph_agentic.ui.uiconfig import UIConfig

class LoadStreamlitUI:
    def __init__(self):
        self.ui_config = UIConfig()
        self.user_controls={}
    def load_streamlit_ui(self):
        title = self.ui_config.get_page_title()
        st.set_page_config(page_title=f"🤖 {title}", layout="wide")
        st.header(f"🤖 {title}")

        with st.sidebar:
            llm_options = self.ui_config.get_llm_options()
            usecase_options = self.ui_config.get_usecase_options()
            self.user_controls['llm_choice'] = st.selectbox("Select LLM Model", llm_options)
            if self.user_controls['llm_choice'] == "GROQ":
                # Model selection for GROQ
                groq_model_options = self.ui_config.get_groq_model_options()
                self.user_controls['groq_model_choice'] = st.selectbox("Select GROQ Model", groq_model_options)
                self.user_controls['GROQ_API_KEY'] = st.session_state["GROQ_API_KEY"] = st.text_input("Enter your GROQ API Key", type="password", key="groq_api_key")
            
                if not self.user_controls.get('llm_choice') == "GROQ":
                    st.warning("Please select an LLM model to proceed.")
                if not self.user_controls['GROQ_API_KEY'] :
                    st.warning("GROQ API Key is required for GROQ LLM.")
            
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)
        return self.user_controls