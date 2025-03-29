from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import os

from services.convo_verifier import is_convo_good_faith
from services.troll_response import troll_response

load_dotenv()
api_key = os.getenv('open_ai_key')


llm = ChatOpenAI(model_name="gpt-4o", temperature=0.9, openai_api_key=api_key)


# we want to verify that the last question is relevant to the topic
# if not, troll the user
# if so, continue
def ask_chatbot(user_messages):
  
  valid_chain = is_convo_good_faith(user_messages)
  if not valid_chain:
    return troll_response(user_messages)
  
  system_message="You are a helpful student advisor assistant. You will help computer science students with their questions about course selection."
  messages = [{"role": "system", "content": system_message}]
  for message in user_messages:
      messages.append({"role": message["role"], "content": message["content"]})

  response = llm.invoke(messages)
  print("\nLLM Response:")
  print(response.content)
  return response.content
    
  
# ask_chatbot(convo)
    
    