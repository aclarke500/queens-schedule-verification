from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import os

from services.convo_verifier import is_convo_good_faith
from services.troll_response import troll_response
from services.context.builder import build_context

load_dotenv()
api_key = os.getenv('deepseek_key')


llm = ChatDeepSeek(model_name="deepseek-chat", temperature=0, api_key=api_key)
prompt = ChatPromptTemplate([
    ("system", """
You are a smart and helpful academic advisor chatbot for Queen’s University School of Computing. 
You specialize in answering student questions about programs, specializations, courses, and degree planning.


Your instructions:
- Always respond using the provided `context`. It contains official academic rules, course lists, and notes. Do not assume any outside information about anything relating to Computing at Queen's.
- Answer the questions with specifics, and assume every student is in the Computing program and therefore needs to satisfy the course requirements. Where possible use course codes and the course title.
- Be direct and informative — like a great TA who knows how to help.
- NEVER make up academic policy or course info that isn’t in the context.
- Be concise but friendly.
- Do not format your answers in lists. There is no markdown. Be conversational in your response.

Your response must be a JSON object like:
{{
  "message": "Here's what you need to know about the AI option..."
}}
"""
),
    ("human", "Here is the conversation so far: {message}Here is the context to answer the prompt:{context}")
])
parser = StructuredOutputParser.from_response_schemas([ResponseSchema(name="message", description="String. The answer to the users question following the context.")])
chain = prompt | llm | parser



def ask_chatbot(user_messages):
    """Processes user messages and returns an AI-generated response.

    This function checks if the conversation is in good faith, builds relevant context,
    and generates an appropriate response using the language model chain.

    Args:
        user_messages: A list of message dictionaries containing the conversation history.
            Each message should have 'role' and 'content' keys.

    Returns:
        str: The AI-generated response message.
            If conversation is deemed not in good faith, returns a troll response instead.

    Raises:
        None
    """
    # check if its a valid question, troll otherwise
    valid_chain = is_convo_good_faith(user_messages)
    if not valid_chain:
        return troll_response(user_messages)
    
    # get our context for the response so LLM knows what to say (RAG is in here)
    context = build_context(user_messages)
    response = chain.invoke({"message":user_messages, "context":context}) # prompt the LLM with context

    return response["message"]
