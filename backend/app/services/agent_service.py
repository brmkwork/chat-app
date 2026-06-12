import os

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from app.tools.read_file_tool import read_file_tool
from app.tools.rag_search_tool import rag_search_tool

load_dotenv()

llm = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY"),
)

tools = [
    read_file_tool,
    rag_search_tool
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a document assistant.

Use read_file_tool when:
- user asks to read the file
- user asks what is in the file
- user asks to display the document
- user asks for complete contents

Use rag_search_tool when:
- user asks questions about the file
- user wants information extracted
- user wants summaries

Always choose the most appropriate tool.
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
    verbose=True
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