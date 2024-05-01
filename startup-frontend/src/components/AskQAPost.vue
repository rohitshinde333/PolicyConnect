<template>
    <div class="qa-post-form-container">
      <h3 style="margin-left: 300px;">Ask a Q&A Post:</h3>
      <form @submit.prevent="submitQAPost" class="qa-post-form">
        <div class="form-group">
          <label for="title">Title:</label>
          <input v-model="questioinsForm.title" id="title" required>
        </div>
        <div class="form-group">
          <label for="content">Content:</label>
          <textarea v-model="questioinsForm.content" id="content" required></textarea>
        </div>
        <button type="submit" class="submit-button">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapGetters } from 'vuex';
  
  export default {
    data() {
      return {
        questioinsForm: {
          title: '',
          content: '',
        },
      };
    },
    computed: {
      ...mapGetters(['accessToken']),
    },
    methods: {
      async submitQAPost() {
        try {
          const response = await axios.post('http://localhost:5000/qa_list', this.questioinsForm, {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          });
          this.$router.push({ name: 'qa_post', params: { id: response.data.id } });
        } catch (error) {
          console.error('Failed to create question:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .qa-post-form-container {
    max-width: 600px;
    margin-left: 70px;
  }
  
  .qa-post-form {
    display: grid;
    gap: 15px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
  }
  
  input,
  textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .submit-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .submit-button:hover {
    background-color: #0056b3;
  }
  </style>
  