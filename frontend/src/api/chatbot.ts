import { store } from '../store'
import { Message, ChatPromptTemplate } from '../types';



function convertMessagesToChatPrompt(messages:Message[]):ChatPromptTemplate[]{
    let chatPrompts: ChatPromptTemplate[] = [];
    messages.forEach(message=>{
        const role =  message.isUser ? "user"  : "assistant";
        chatPrompts.push({
            role:role,
            content:message.text
        })
    })

    return chatPrompts
}


export async function askChatbot(messages:Message[]){
    const history = convertMessagesToChatPrompt(messages)
    const apiUrl = store.apiUrl();
    const fullEndpoint: string = apiUrl +'/api/chatbot';
    // debugger
    const response = await fetch(fullEndpoint, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({history})
    })

    if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data)
    const llmMessage = data?.llm_response;
    return llmMessage;
}