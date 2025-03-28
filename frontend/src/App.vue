<script setup lang="ts">
// No script needed in the main App component as state is now managed by the store
</script>

<template>
  <div class="app-container">
    <div class="content-wrapper">
      <div class="header">
        <img src="https://media1.giphy.com/media/ieJdVmYjqq6SA09qgb/giphy_s.gif" alt="Queen's Bear" class="logo">
        <h1 class="title">
          Queen's Schedule Analyzer
        </h1>
        <img src="https://i.ibb.co/3Y1m7CJm/boohoo-removebg-preview.png" alt="boohoo the bear" class="logo">
      </div>

      <!-- Router view will display either UploadPage or ResultsPage -->
      <router-view />
    </div>
  </div>
</template>

<style lang="scss">
// Variables - Enhanced color palette
$queens-yellow: #ffcb05; // Brighter yellow
$queens-blue: #0375b4; // More vibrant blue
$queens-red: #e61c2b; // More vibrant red
$dark-bg-1: #1a1f36; // Richer dark blue
$dark-bg-2: #252d47; // Improved midtone
$dark-bg-3: #343c5a; // Lighter card background
$text-light: #ffffff;
$text-light-muted: #b0c0d6; // More bluish light gray
$accent-purple: #6b56c6; // Additional accent color
$card-gradient-start: rgba(23, 28, 56, 0.7);
$card-gradient-end: rgba(32, 40, 68, 0.9);

// Main container
.app-container {
  min-height: 100vh;
  padding: 1rem;
  background: linear-gradient(135deg, $dark-bg-1, darken($dark-bg-1, 8%));
  font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  color: $text-light;

  @media (min-width: 768px) {
    padding: 2rem;
  }
}

.content-wrapper {
  max-width: 1024px;
  margin: 0 auto;
}

// Header section
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.logo {
  width: 6rem;
  height: 6rem;
  object-fit: cover;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
}

.title {
  font-size: 2.25rem;
  font-weight: 800;
  color: $queens-yellow;
  text-align: center;
  text-shadow: 0 2px 15px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.5px;
  
  @media (min-width: 768px) {
    font-size: 3.5rem;
  }
}

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

// Results section
.results-section {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.results-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.results-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.results-title {
  font-size: 2rem;
  font-weight: 800;
  color: $queens-yellow;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

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

.requirements-title {
  color: $queens-yellow;
  
  &::after {
    background-color: $queens-blue;
  }
}

// Courses list
.courses-container, .requirements-container {
  background: linear-gradient(165deg, $card-gradient-start, $card-gradient-end);
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  margin-bottom: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.course-card {
  padding: 1.75rem;
  background: linear-gradient(145deg, rgba($dark-bg-3, 0.7), rgba($dark-bg-3, 0.9));
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.03);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    border-color: rgba($queens-blue, 0.3);
  }
}

.course-code {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  color: $queens-blue;
  letter-spacing: -0.5px;
}

.course-time {
  font-size: 1.25rem;
  color: $text-light;
  font-weight: 500;
  background-color: rgba($queens-blue, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  display: inline-block;
  margin-bottom: 0.75rem;
}

.course-location {
  font-size: 1.125rem;
  color: $text-light-muted;
  margin-top: 0.75rem;
  padding-left: 0.5rem;
  border-left: 3px solid $queens-red;
}

// Requirements list
.requirements-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1rem;
}

.requirement-item {
  font-size: 1.25rem;
  font-weight: 600;
  color: $queens-red;
  text-align: center;
  padding: 1rem;
  background-color: rgba($queens-red, 0.08);
  border-radius: 0.75rem;
  border: 1px solid rgba($queens-red, 0.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-3px);
    background-color: rgba($queens-red, 0.12);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  }
}
</style>