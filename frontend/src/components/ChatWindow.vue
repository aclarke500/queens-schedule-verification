<script setup lang="ts">
import { reactive } from 'vue'
import { askChatbot } from '../api/chatbot'
import { Message } from '../types'

interface ChatState {
  messages: Message[]
  newMessage: string
  isLoading: boolean
}

const state = reactive<ChatState>({
  messages: [],
  newMessage: '',
  isLoading: false
})

const sendMessage = async () => {
  if (!state.newMessage.trim()) return
  
  // Add user message
  state.messages.push({
    text: state.newMessage,
    isUser: true,
    timestamp: new Date()
  })
  
  // Show loading state
  state.isLoading = true
  const newMessage = await askChatbot(state.messages)
  
  // Simulate bot response with 2 second delay

    state.messages.push({
      text: newMessage,
      isUser: false,
      timestamp: new Date()
    })
    state.isLoading = false

  
  state.newMessage = ''
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>Queen's CS Course Chatbot</h2>
    </div>
    
    <div class="chat-messages">
      <div v-for="(message, index) in state.messages" 
           :key="index" 
           :class="['message', message.isUser ? 'user-message' : 'bot-message']">
        <div class="message-content">
          {{ message.text }}
        </div>
        <div class="message-time">
          {{ message.timestamp.toLocaleTimeString() }}
        </div>
      </div>
      
      <!-- Typing indicator -->
      <div v-if="state.isLoading" class="message bot-message typing-indicator">
        <div class="message-content">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <input 
        v-model="state.newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
        type="text"
        :disabled="state.isLoading"
      >
      <button @click="sendMessage" :disabled="state.isLoading">Send</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.chat-container {
  background: linear-gradient(145deg, rgba(23, 28, 56, 0.7), rgba(32, 40, 68, 0.9));
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  height: 500px;
  overflow: hidden;
}

.chat-header {
  padding: 1rem 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  
  h2 {
    margin: 0;
    color: #ffcb05;
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  position: relative;
  
  &.user-message {
    align-self: flex-end;
    background: linear-gradient(135deg, #0375b4, darken(#0375b4, 15%));
    color: white;
    border-bottom-right-radius: 0.25rem;
  }
  
  &.bot-message {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    border-bottom-left-radius: 0.25rem;
  }
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.25rem;
  text-align: right;
}

.typing-indicator {
  .message-content {
    display: flex;
    gap: 0.25rem;
    padding: 0.5rem 1rem;
    
    span {
      width: 8px;
      height: 8px;
      background: rgba(255, 255, 255, 0.7);
      border-radius: 50%;
      animation: typing 1s infinite ease-in-out;
      
      &:nth-child(2) {
        animation-delay: 0.2s;
      }
      
      &:nth-child(3) {
        animation-delay: 0.4s;
      }
    }
  }
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  
  input {
    flex: 1;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }
    
    &:focus {
      outline: none;
      border-color: #0375b4;
    }
  }
  
  button {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    border: none;
    background: linear-gradient(135deg, #ffcb05, darken(#ffcb05, 15%));
    color: #1a1f36;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(255, 203, 5, 0.3);
    }
  }
  
  input, button {
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}
</style>
