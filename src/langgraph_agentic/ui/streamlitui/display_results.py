import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage    
import json
class DisplayResults:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_basic_chatbot_results(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase == "Simple ChatBot":
            print ("process start")
        
            with st.chat_message("user"):
                st.write(user_message)
            response = graph.stream({"messages":("user",user_message)},stream_mode = "values")##this will stream first human only message state 
                #and then new state with ai message along with human message

            last_ai_message = None
            for event in response:
                last_ai_message = event

            # print("Final AI Message:")
            # print(last_ai_message)

            with st.chat_message("assistant"):
                st.write(last_ai_message["messages"][1].content.split("</think>")[-1].strip())  ##display only the last ai message content        
            








            # response = graph.stream({"messages":("user",user_message)},stream_mode = "updates")##this will stream first human only message state 
            #     #and then new state with ai message along with human message
            # last = None
            # for x in response:
            #     last =  x
            # print(last)                                                                    //All this code is used if i use the method updates instead of values for streaming
            # with st.chat_message("assistant"):
            #     st.write(last["chatbot"]["messages"][0].content)  ##display only the last ai message content