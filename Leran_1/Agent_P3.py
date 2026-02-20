from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage #Passes data back to LLM after it calls a tool such as the content
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

"""BaseMessage -> The foundational class for all message types in LangGraph
        BaseMessage is a parent class and all are child class these are inharitate all properties from parent class or
        from BaseMessage.
   ToolMessage -> Passes data back to LLM after it calls a tool such as the content.
   TypedDict -> defines a dictionary type with a fixed set of keys and specific value types.
   Annotated -> provide additional context to your variable without affecting the type/datatype itself.
   email = Annotated[str, "This has to be a valid email format!"]
   print(email.__metadata__)
   Sequence -> To automatically handle the state updates for sequence such as by adding new messages to a chat history
"""

load_dotenv()