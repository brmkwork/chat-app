import os

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from app.tools.search_local_files_tool import search_local_files_tool
from app.tools.read_file_tool import read_file_tool
from app.tools.load_file_tool import load_file_tool
from app.tools.rag_search_tool import rag_search_tool

load_dotenv()

llm = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY"),
)

tools = [
    search_local_files_tool,
    read_file_tool,
    load_file_tool,
    rag_search_tool
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
    """
    You are a local file assistant.

    Available tools:

    search_local_files_tool
    - Find files on the user's machine.

    read_file_tool
    - Read the entire contents of a file.

    load_file_tool
    - Load a file into the vector database.

    rag_search_tool
    - Answer questions about a previously loaded file.

    Rules:

    If the user asks to find a file:
    use search_local_files_tool

    If the user asks to read a file:
    first find the file
    then read it

    If the user asks questions about a file:
    load it first
    then use rag_search_tool

    Never make up file paths.
    Always use tools.
    choose the most appropriate tool.
"""
        ),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False
)

def ask_agent(
    conversation_id: int,
    user_input: str
) -> str:

    result = agent_executor.invoke(
        {
            "input": (
                f"Conversation ID: {conversation_id}\n"
                f"Question: {user_input}"
            )
        }
    )

    return result["output"]