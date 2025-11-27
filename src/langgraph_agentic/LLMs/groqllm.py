import os 
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
        
    def get_model(self):
        try:
            groq_api_key = self.user_controls_input['GROQ_API_KEY']
            groq_model = self.user_controls_input['groq_model_choice']

            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is required to initialize Groq LLM.")

            return ChatGroq(api_key=groq_api_key, model=groq_model)

        except Exception as e:
            st.error(f"Error initializing Groq LLM: {e}")
            return None
