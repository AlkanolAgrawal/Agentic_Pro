from langgraph.graph import StateGraph,START,END
from src.langgraph_agentic.nodes.basic_chatbot import BasicChatbot
from src.langgraph_agentic.state.state import State


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_builder(self):
        """Builds a basic chatbot graph structure."""


        self.basic_chatbot = BasicChatbot(self.llm)


        self.graph_builder.add_node("chatbot",self.basic_chatbot.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def setup_graph(self,usecase:str):
        if usecase == "Simple ChatBot":
            self.basic_chatbot_builder()
        return self.graph_builder.compile()