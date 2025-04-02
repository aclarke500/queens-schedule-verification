from services.context.context_planning import get_context_retrieval_flags
from services.context.get_courses import get_course_context
from services.context.program import get_program_context
from services.context.RAG import get_general_context


def build_context(chat_history: str) -> str:
    """Builds context for the chat response based on chat history.

    This function analyzes the chat history and retrieves relevant context by:
    1. Getting context retrieval flags to determine what info is needed
    2. Looking up course-specific context if needed
    3. Getting program requirement context
    4. Getting general context from RAG system

    Args:
        chat_history: String containing the conversation history with the user

    Returns:
        String containing the combined context from all sources that will help
        inform the response
    """
    flags = get_context_retrieval_flags(chat_history)
    context = ''
    if flags["lookup_courses"]:
        course_context = get_course_context(chat_history)
        context += course_context
    
    program_context = get_program_context(chat_history)
    context += program_context

    general_context = get_general_context(chat_history)
    context += general_context
    
    return context
