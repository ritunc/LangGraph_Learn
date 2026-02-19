### Agent I

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os


load_dotenv()

# os.environ[]

class AgentState(TypedDict):
        messages:List[HumanMessage]


# llm = ChatGroq(model="meta-llama/llama-prompt-guard-2-86m")
llm = ChatGroq(model="llama-3.3-70b-versatile")
print(llm)

def process(state: AgentState) -> AgentState:
        response = llm.invoke(state["messages"])
        print(f"\nAI: {response.content}")
        # return {"messages":response}
        return state

graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.add_edge(START, "process")
graph.add_edge("process",END)

app = graph.compile()

# user_input = input("Enter the text...")

# app.invoke({"messages": [HumanMessage(content=user_input)]})
user_input = input("Enter: ")
while user_input != "exit":
        app.invoke({"messages": [HumanMessage(content=user_input)]})
        user_input = input("Enter: ")

# result = app.invoke({"messages": [HumanMessage(content=user_input)]})

# print(result)