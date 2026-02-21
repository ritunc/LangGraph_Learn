"""Agent-IV   mini Project DRAFTER"""

from typing import Annotated, TypedDict, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# Global variable to store document content
document_content = ""

class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str) -> str:
        """Updates the document with the provided content."""
        global document_content
        document_content = content
        return f"Document has been updated successfully! The current content is:\n{document_content}"


@tool
def save(filename: str) -> str:
        """Save the current document to a text file and finish the process

        Args:
           filename: Name for the text file.
        """
        global document_content

        if not filename.endswith('.txt'):
                filename = f"{filename}.txt"
        
        try:
                with open(filename, 'w') as file:
                        file.write(document_content)
                print(f"\n🗃️ Document has been saved successfully to: {filename}")
                return f"Document has been saved successfully to '{filename}'."
        except Exception as error:
                return f"Error saving document: {str(error)}"

tools = [update, save]

model = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)


def our_agent(state: AgentState) -> AgentState:
        SYSTEM_PROMPT = """
        You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.

        - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
        - If the user wants to save and finish, you need to use the 'save' tool.
        - Make sure to always show the current document state after modifications.

        The current document content is:{document_content}

        """
        system_prompt = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = model.invoke(system_prompt)
        return {"messages":[response]}

