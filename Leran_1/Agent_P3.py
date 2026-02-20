"""Agent-III"""
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
        from BaseMessage. This is a LangChain standard class representing a message, 
        such as HumanMessage, AIMessage, or ToolMessage. It's contain all those data-type together.
   ToolMessage -> Passes data back to LLM after it calls a tool such as the content.
   TypedDict -> defines a dictionary type with a fixed set of keys and specific value types.
   Annotated -> provide additional context to your variable without affecting the type/datatype itself.
   email = Annotated[str, "This has to be a valid email format!"]
   print(email.__metadata__)
   Sequence -> To automatically handle the state updates for sequence such as by adding new messages to a chat history.
        It is a type hint used to indicate that a variable, function argument, or return value is an ordered collection 
        that supports indexing and length checks, without restricting it to a specific mutable or immutable type 
        like list or tuple. This tells Python that the messages key in your state should be treated as an ordered 
        list (or sequence) of these message objects.
   add_messages -> Rule that controls how updates from nodes are combined with the
        existing state. Tells us how to merge new data into the current state
        without a reducer, updates would have replaced the existing value entirely!
"""

load_dotenv()

class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
        """This is an addition function that adds 2 numbers together"""
        return a+b

tools = [add]

model = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)

# LLM calling function
def model_call(state: AgentState) -> AgentState:
        message = state["messages"]
        SYSTEM_PROMPT="You are my AI assistant, please answer my query to the best of your ability."
        system_message = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

        response = model.invoke(system_message)
        return {"messages":[response]}


# condition function
def should_continue(state: AgentState):
        message = state["messages"]
        last_message = message[-1]
        if not last_message.tool_calls:
                return "end"
        else:
                return "continue"


# Initiat the GRaph
graph = StateGraph(AgentState)

graph.add_node("agent", model_call)
# tool_node = ToolNode(tools=tools)
# graph.add_node("tools", ToolNode(tool_node))
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_conditional_edges(
        "agent",
        should_continue,
        {
                "continue":"tools",
                "end":END
        }
)
graph.add_edge("tools", "agent")

app = graph.compile()


def print_stream(stream):
        for s in stream:
                message = s["messages"][-1]
                if isinstance(message, tuple):
                        print(message)
                else:
                        message.pretty_print()


# inputs = {"messages":[("user", "Add 3 + 4.")]}
inputs = {"messages":"Add 3 + 4."}
print_stream(app.stream(inputs, stream_mode="values"))