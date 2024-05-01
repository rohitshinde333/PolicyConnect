<template>
    <div class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading...</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingSpinner',
  };
  </script>
  
  <style scoped>
  .loading-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-size: 24px;
  }
  
  .fa-spinner {
    font-size: 48px;
    animation: spin 2s infinite linear;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>
  