<script setup lang="ts">
import { useRouter } from 'vue-router';
import { store } from '../store';
import ChatWindow from '../components/ChatWindow.vue';

const router = useRouter();

const handleFileUpload = (semester: 'fall' | 'winter', event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    if (semester === 'fall') {
      store.setFallSchedule(target.files[0]);
    } else {
      store.setWinterSchedule(target.files[0]);
    }
  }
};

const analyzeSchedules = async () => {
  await store.analyzeSchedules();
  router.push('/results');
};
</script>

<template>
  <div class="upload-section">
    <div class="chat-section">
      <h2 class="section-title">Need Help?</h2>
      <ChatWindow />
    </div>
    <div class="semester-uploads">
      <div class="semester-container">
        <h2 class="semester-title">Fall Semester</h2>
        <div class="upload-box" :class="{ 'has-file': store.fallSchedule }">
          <label class="upload-label">
            <input
              type="file"
              accept="image/*"
              class="file-input"
              @change="(e) => handleFileUpload('fall', e)"
            >
            <div class="upload-content">
              <div v-if="store.fallSchedule" class="file-name">
                {{ store.fallSchedule.name }}
              </div>
              <div v-else class="upload-prompt">
                <span class="upload-text">Click to upload</span>
                <p class="upload-description">Upload your fall semester schedule</p>
              </div>
            </div>
          </label>
        </div>
      </div>

      <div class="semester-container">
        <h2 class="semester-title">Winter Semester</h2>
        <div class="upload-box" :class="{ 'has-file': store.winterSchedule }">
          <label class="upload-label">
            <input
              type="file"
              accept="image/*"
              class="file-input"
              @change="(e) => handleFileUpload('winter', e)"
            >
            <div class="upload-content">
              <div v-if="store.winterSchedule" class="file-name">
                {{ store.winterSchedule.name }}
              </div>
              <div v-else class="upload-prompt">
                <span class="upload-text">Click to upload</span>
                <p class="upload-description">Upload your winter semester schedule</p>
              </div>
            </div>
          </label>
        </div>
      </div>
    </div>

    <div class="action-container">
      <button
        class="analyze-button"
        :disabled="!store.canAnalyze || store.loading"
        @click="analyzeSchedules"
      >
        <span v-if="store.loading">Analyzing...</span>
        <span v-else>Analyze Schedules</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Styles will be imported from the main stylesheet */
</style> 