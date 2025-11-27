from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated,List


class State(TypedDict):
    messages:Annotated[List,add_messages]