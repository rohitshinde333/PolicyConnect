<template>
    <div class="modal" v-if="isOpen">
      <div class="modal-content">
        <h2>{{ title }}</h2>
        <p>{{ message }}</p>
        <button @click="closeModal">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['title', 'message', 'isOpen'],
    methods: {
      closeModal() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .modal-content {
    background-color: white;
    padding: 2rem;
    border-radius: 4px;
  }
  </style>
  