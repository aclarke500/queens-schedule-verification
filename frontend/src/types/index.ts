
export interface Message {
    text: string
    isUser: boolean
    timestamp: Date
}

export interface ChatPromptTemplate {
    role:"user" | "assistant",
    content:string
}
