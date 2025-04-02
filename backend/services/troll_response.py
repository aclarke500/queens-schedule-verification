from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

api_key = os.getenv("open_ai_key")

# LLM
troll_llm = ChatOpenAI(model_name="gpt-4o", temperature=1.0, openai_api_key=api_key)

troll_prompt = ChatPromptTemplate.from_messages([
    ("system","A user has been messaging our chatbot in bad faith. Please give them snarky responses and call them a silly frosh and tell them they can only ask questions about academic advising for CS at Queen's,"),
    ("user", "{history}")
    ])

troll_chain = troll_prompt | troll_llm

def troll_response(user_messages:list[str])->str:
    history = ' '.join(msg["content"] for msg in user_messages)
    
    response = troll_chain.invoke({"history":history})
    return response.content

