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

<style lang="scss" scoped>
// Variables - Enhanced color palette
$queens-yellow: #ffcb05;
$queens-blue: #0375b4;
$queens-red: #e61c2b;
$dark-bg-1: #1a1f36;
$dark-bg-2: #252d47;
$dark-bg-3: #343c5a;
$text-light: #ffffff;
$text-light-muted: #b0c0d6;
$card-gradient-start: rgba(23, 28, 56, 0.7);
$card-gradient-end: rgba(32, 40, 68, 0.9);

// Upload section
.upload-section {
  display: flex;
  flex-direction: column;
  gap: 3.5rem;
}

.semester-uploads {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
  
  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr;
  }
}

.semester-container {
  display: flex;
  flex-direction: column;
}

.semester-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: $queens-blue;
  text-align: center;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 3px;
    background-color: $queens-yellow;
    border-radius: 3px;
  }
}

.upload-box {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(145deg, $card-gradient-start, $card-gradient-end);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  
  &:hover {
    transform: translateY(-5px);
    border-color: rgba($queens-yellow, 0.5);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  }
  
  &.has-file {
    border-style: solid;
    border-color: $queens-blue;
    background: linear-gradient(145deg, rgba($queens-blue, 0.1), rgba($queens-blue, 0.05));
  }
}

.upload-label {
  display: block;
  width: 100%;
  cursor: pointer;
}

.file-input {
  display: none;
}

.upload-content {
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.file-name {
  font-size: 1.125rem;
  color: $text-light;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  word-break: break-all;
}

.upload-prompt {
  .upload-text {
    font-size: 1.4rem;
    font-weight: 700;
    color: $queens-yellow;
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .upload-description {
    font-size: 1.125rem;
    color: $text-light-muted;
    margin-top: 1rem;
  }
}

// Action buttons
.action-container {
  text-align: center;
  margin-top: 1rem;
}

.analyze-button {
  background: linear-gradient(135deg, $queens-red, darken($queens-red, 15%));
  color: $text-light;
  font-weight: 700;
  font-size: 1.25rem;
  padding: 1.15rem 2.5rem;
  border-radius: 0.75rem;
  border: none;
  box-shadow: 0 15px 25px rgba($queens-red, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0));
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover:not(:disabled) {
    transform: translateY(-5px);
    box-shadow: 0 20px 35px rgba($queens-red, 0.4);
    
    &::before {
      opacity: 1;
    }
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: linear-gradient(135deg, desaturate($queens-red, 30%), darken(desaturate($queens-red, 30%), 15%));
    box-shadow: 0 10px 20px rgba(darken($queens-red, 30%), 0.2);
  }
}

// Section title
.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: $queens-blue;
  text-align: center;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background-color: $queens-yellow;
    border-radius: 3px;
  }
}
</style> 