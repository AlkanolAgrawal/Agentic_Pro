class BasicChatbot:
    def __init__(self, model):
        self.llm = model

    def process(self, state) -> dict:
        response = self.llm.invoke(state["messages"])
        return {
            "messages": [response]
        }
