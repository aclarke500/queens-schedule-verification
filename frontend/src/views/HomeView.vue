<script setup lang="ts">
// No additional setup needed
</script>

<template>
  <div class="home-container">
    <div class="feature-grid">
      <div class="feature-card">
        <h2>Schedule Checker</h2>
        <p>Upload your Queen's course schedules and get instant feedback on potential conflicts, missing requirements, and optimization suggestions.</p>
        <router-link to="/upload" class="feature-link">Check Your Schedule →</router-link>
      </div>

      <div class="feature-card">
        <h2>Course Chatbot</h2>
        <p>Get personalized course advice, learn about prerequisites, and explore program requirements through our AI-powered chatbot assistant.</p>
        <router-link to="/chat" class="feature-link">Chat About Courses →</router-link>
      </div>
    </div>

    <div class="info-section">
      <p class="disclaimer">This tool is designed to assist Queen's University students in planning their academic schedules. While we strive for accuracy, always verify information with official university resources.</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
// Variables to match App.vue
$queens-yellow: #ffcb05;
$queens-blue: #0375b4;
$text-light: #ffffff;
$text-light-muted: #b0c0d6;
$card-gradient-start: rgba(23, 28, 56, 0.7);
$card-gradient-end: rgba(32, 40, 68, 0.9);

.home-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: calc(100vh - 300px); // Reduced from 100vh
  display: flex;
  flex-direction: column;
}

.feature-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  background: linear-gradient(145deg, $card-gradient-start, $card-gradient-end);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);

  h2 {
    color: $queens-yellow;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
  }

  p {
    color: $text-light-muted;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }
}

.feature-link {
  color: $queens-blue;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;

  &:hover {
    color: $queens-yellow;
  }
}

.info-section {
  text-align: center;
  margin-top: auto;
  padding-top: 3rem;
  padding-bottom: 2rem; // Added padding at the bottom

  .disclaimer {
    color: $text-light-muted;
    font-size: 0.9rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
  }
}
</style>
