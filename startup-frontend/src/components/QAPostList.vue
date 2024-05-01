<template>
  <div class="qa-posts-container">
    <h3>Q&A Posts:</h3>
    <div v-for="qa_post in qa_posts" :key="qa_post.id" class="qa-post-item">
      <div class="qa-post-content">
        <h4 class="qa-post-title">{{ qa_post.title }}</h4>
        <p class="qa-post-text">{{ qa_post.content }}</p>
        <button @click="deleteQuestion(qa_post.id)" class="btn btn-danger">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      qa_posts: [],
    };
  },
  mounted() {
    this.fetchQAPosts();
  },
  methods: {
    async fetchQAPosts() {
      try {
        const response = await axios.get('http://localhost:5000/qa_list');
        this.qa_posts = response.data;
      } catch (error) {
        console.error('Failed to fetch Q&A posts:', error);
      }
    },
    async deleteQuestion(questionId) {
      try {
        await axios.delete(`http://localhost:5000/qa_list/${questionId}`);
        this.fetchQAPosts();
      } catch (error) {
        console.error('Failed to delete question:', error);
      }
    },
  },
};
</script>

<style scoped>
.qa-posts-container {
  max-width: 800px;
  margin: 0 auto;
}

.qa-post-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 15px;
}

.qa-post-content {
  width: 100%;
}

.qa-post-title {
  margin-bottom: 10px;
  color: #333;
}

.qa-post-text {
  color: #555;
}

.btn-danger {
  margin-top: 10px;
}
</style>
