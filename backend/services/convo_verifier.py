from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
import os

api_key = os.getenv("open_ai_key")

# LLM + parser
convo_verifier_llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)
convo_verifier_parser = StructuredOutputParser.from_response_schemas([
    ResponseSchema(name="is_good_faith", description="'True' or 'False'")
])

# Prompt template
convo_verifier_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are deciding whether a user of a Queen's University academic advisor chatbot is engaging in good faith.
You will be given the conversation history. If the user appears to be asking relevant, respectful, and helpful academic questions, return {{"is_good_faith": "True"}}.
If the user is being silly, rude, or trying to break the system (e.g., asking about food, jokes, ChatGPT hacks, etc.), return {{"is_good_faith": "False"}}.
Always respond ONLY with the JSON output."""),
    ("user", "{history}")
])

# Pipe together
convo_verifier_chain = convo_verifier_prompt | convo_verifier_llm | convo_verifier_parser

# Usage function
def is_convo_good_faith(user_messages: list[str]) -> bool:
    # Create history string without leading comma
    history = ' '.join(msg["content"] for msg in user_messages)
    
    result = convo_verifier_chain.invoke({"history": history})
    return result["is_good_faith"].lower() == "true"
