<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { store } from '../store';

const router = useRouter();

onMounted(() => {
  // If no analysis result exists, redirect to upload page
  if (!store.analysisResult) {
    router.push('/');
  }
});

const goBack = () => {
  store.resetState();
  router.push('/');
};
</script>

<template>
  <div v-if="store.analysisResult" class="results-section">
    <div class="results-container">
      <div class="requirements-container">
        <h3 class="section-title requirements-title">Requirements Check</h3>
        <ul class="requirements-list">
          <li v-for="requirement in store.analysisResult.cs_requirements" 
              :key="requirement"
              class="requirement-item">
            {{ requirement }}
          </li>
        </ul>
      </div>

      <div class="courses-container">
        <h3 class="section-title">Your Courses</h3>
        <div class="course-list">
          <div v-for="course in store.analysisResult.courses" :key="course.course_code" 
                class="course-card">
            <h4 class="course-code">{{ course.course_code }}</h4>
            <p class="course-time">
              {{ course.day }} | {{ course.time_start }} - {{ course.time_end }}
            </p>
            <p class="course-location">{{ course.location }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="action-container">
      <button class="analyze-button" @click="goBack">
        Analyze Another Schedule
      </button>
    </div>
  </div>
  <div v-else class="loading-container">
    <p>No analysis data available. Redirecting to upload page...</p>
  </div>
</template>

<style scoped>
/* Styles will be imported from the main stylesheet */
.loading-container {
  text-align: center;
  padding: 2rem;
  color: white;
  font-size: 1.25rem;
}
</style> 