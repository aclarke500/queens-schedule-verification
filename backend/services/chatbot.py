from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import os

from services.convo_verifier import is_convo_good_faith
from services.troll_response import troll_response
from services.RAG import get_n_chunks
from prompts.prompts import chatbot_prompt, rag_prompt

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

    # Step 2: Prepare context
    last_user_message = user_messages[-1]["content"]
    context = get_n_chunks(last_user_message)
   
    messages = []
    # Inject RAG-based system message
    messages.append({
        "role": "system",
        "content":chatbot_prompt
    })

    # Add prior assistant/user turns (before the last user message)
    messages.extend(user_messages[:-1])
    
    
    
    # Inject context + last user message
    messages.append({
      "role":"system",
      "content":rag_prompt+context
    })
    messages.append(
    {
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {last_user_message}"
    })



    # Step 4: Call LLM
    response = llm.invoke(messages)
    print("\nLLM Response:")
    print(response.content)

    return response.content

    
  
# ask_chatbot(convo)
    
    