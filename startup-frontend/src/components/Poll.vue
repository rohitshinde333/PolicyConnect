<template>
  <div v-if="poll" class="poll-details">
    <h2 class="poll-title">{{ poll.title }}</h2>
    <p class="poll-description">{{ poll.description }}</p>

    <div v-for="question in poll.questions" :key="question.id" class="question-container">
      <h4 class="question-text">{{ question.text }}</h4>
      <ul class="options-list">
        <li v-for="option in question.options" :key="option.id" class="option-item">
          <div class="option-container">
            <div class="option-text">{{ option.text }}</div>
            <button @click="deleteOption(option.id)" class="delete-option-button">Delete</button>
          </div>
        </li>
      </ul>
      <div class="add-option-container">
        <input type="text" v-model="newOptionText" placeholder="Enter new option" class="new-option-input">
        <button @click="addOption(question.id)" class="add-option-button">Add Option</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapActions } from 'vuex';
export default {
  data() {
    return {
      poll: null,
      newOptionText: '',
    };
  },
  computed: {
    ...mapGetters(['accessToken']),
  },
  mounted() {
    this.fetchPollDetails();
  },
  methods: {
    ...mapActions(['clearAccessToken']),
    fetchPollDetails() {
      const pollId = this.$route.params.id;

      axios
        .get(`http://localhost:5000/polls/${pollId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.poll = response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch poll details:', error);
        });
    },
    addOption(questionId) {
      axios
        .post(`http://localhost:5000/questions/${questionId}/options`, {
          text: this.newOptionText,
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Refresh poll details after adding an option
          this.fetchPollDetails();
          this.newOptionText = ''; // Clear the input field
        })
        .catch((error) => {
          console.error('Failed to add option:', error);
        });
    },
    deleteOption(optionId) {
      axios
        .delete(`http://localhost:5000/options/${optionId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Refresh poll details after deleting an option
          this.fetchPollDetails();
        })
        .catch((error) => {
          console.error('Failed to delete option:', error);
        });
    },
  },
};
</script>

<style scoped>
.poll-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.poll-title {
  font-size: 24px;
  margin-bottom: 10px;
}

.poll-description {
  font-size: 16px;
  margin-bottom: 20px;
}

.question-container {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 20px;
}

.question-text {
  font-size: 18px;
  margin-bottom: 10px;
}

.options-list {
  list-style-type: none;
  padding: 0;
}

.option-item {
  margin-bottom: 15px;
}

.option-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option-text {
  font-size: 16px;
}

.delete-option-button {
  padding: 6px;
  background-color: #f44336;
  color: #fff;
  border: none;
  cursor: pointer;
}

.delete-option-button:hover {
  background-color: #d32f2f;
}

.add-option-container {
  margin-top: 10px;
}

.new-option-input {
  padding: 8px;
  margin-right: 10px;
}

.add-option-button {
  padding: 8px 12px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  cursor: pointer;
}

.add-option-button:hover {
  background-color: #45a049;
}
</style>
