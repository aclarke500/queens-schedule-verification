<script setup lang="ts">
import ChatWindow from '../components/ChatWindow.vue';
</script>

<template>
  <div class="chat-page">
    <ChatWindow />
  </div>
</template>

<style lang="scss" scoped>
.chat-page {
  width: 100%;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  
  :deep(.chat-container) {
    width: 100%;
    max-width: 1200px;
    height: 60vh;
  }

  :deep(.chat-header) {
    padding: 1.5rem 2rem;
    
    h2 {
      font-size: 2.5rem;
      
      @media (max-width: 768px) {
        font-size: 1.8rem;
      }
    }
  }

  :deep(.chat-messages) {
    padding: 2rem;
    
    .message {
      max-width: 600px;
      
      .message-content {
        font-size: 1.1rem;
      }
    }
  }

  :deep(.chat-input) {
    padding: 1.5rem 2rem;
    
    input {
      font-size: 1.1rem;
      padding: 1rem 1.5rem;
    }
    
    button {
      padding: 1rem 2rem;
      font-size: 1.1rem;
    }
  }
}
</style>
