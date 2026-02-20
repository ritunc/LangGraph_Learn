"""Agent I"""

# from typing import TypedDict, List
# from langchain_core.messages import HumanMessage
# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv
# import os


# load_dotenv()

# # os.environ[]

# class AgentState(TypedDict):
#         messages:List[HumanMessage]


# # llm = ChatGroq(model="meta-llama/llama-prompt-guard-2-86m")
# llm = ChatGroq(model="llama-3.3-70b-versatile")
# print(llm)

# def process(state: AgentState) -> AgentState:
#         response = llm.invoke(state["messages"])
#         print(f"\nAI: {response.content}")
#         # return {"messages":response}
#         return state

# graph = StateGraph(AgentState)

# graph.add_node("process", process)

# graph.add_edge(START, "process")
# graph.add_edge("process",END)

# app = graph.compile()

# # user_input = input("Enter the text...")

# # app.invoke({"messages": [HumanMessage(content=user_input)]})
# user_input = input("Enter: ")
# while user_input != "exit":
#         app.invoke({"messages": [HumanMessage(content=user_input)]})
#         user_input = input("Enter: ")

# # result = app.invoke({"messages": [HumanMessage(content=user_input)]})

# # print(result)


"""Agent II Chatbot🧠
   create a form of memory for our agent
"""
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
        messages: List[Union[HumanMessage, AIMessage]]


llm2 = ChatGroq(model="llama-3.3-70b-versatile")

def progress(state: AgentState) -> AgentState:
        """This node for model response based on user query"""

        response = llm2.invoke(state["messages"])
        state["messages"].append(AIMessage(content=response.content))
        print(f"\nAI: {response.content}")
        print("CURRENT STATE: ", state["messages"])

        return state
        # return {"messages":[llm2.invoke(state["messages"])]}


graph = StateGraph(AgentState)

graph.add_node("process", progress)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input1 = input("Enter:")
while user_input1 != "exit":
        """It's kept previous conversation intact and state contain all conversation"""
        conversation_history.append(HumanMessage(content=user_input1))

        result = agent.invoke({"messages": conversation_history})

        # print(result["messages"])
        conversation_history = result["messages"]

        user_input1 = input("Enter-:")

with open("logging.txt", "w") as file:
        file.write("Your Conversation Log:\n")
        for message in conversation_history:
                if isinstance(message, HumanMessage):
                        file.write(f"You: {message.content}\n")
                elif isinstance(message, AIMessage):
                        file.write(f"AI: {message.content}\n\n")
        file.write("End of Conversation")

print("Conversation saved to logging.txt")









