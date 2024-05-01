<template>
  <div class="policy-details-container">
    <div v-if="policy" class="policy-details">
      <!-- Policy details -->
      <h2>{{ policy.title }}</h2>
      <p v-if="!summarizedContent">{{ policy.content }}</p>
      <p v-else>{{ summarizedContent }}</p>
      <p>Likes: {{ policy.likes }}, Dislikes: {{ policy.dislikes }}</p>

      <!-- Button to get summary -->
      <button v-if="!summarizedContent" @click="getSummary" class="btn btn-primary">Get Summary</button>

      <!-- Comment section container (unchanged) -->
      <div class="comment-section-container">
        <div class="comment-section">
          <!-- Comments (unchanged) -->
          <h6>Comments:</h6>
          <ul>
            <li v-for="comment in policy.comments" :key="comment.id">
              <div class="comment">
                <span class="user">{{ comment.user }}:</span>
                {{ comment.comment_text }}
                <button v-if="comment.user_id === currentUserId" @click="deleteComment(comment.id)" class="btn btn-sm btn-danger">Delete</button>
              </div>
            </li>
          </ul>

          <!-- Comment form (unchanged) -->
          <form @submit.prevent="submitComment(policy.id)">
            <div class="form-group">
              <label for="commentText">Add a comment:</label>
              <input type="text" v-model="commentText" class="form-control" id="commentText">
            </div>
            <button type="submit" class="btn btn-primary">Submit Comment</button>
          </form>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading policy details...</p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  data() {
    return {
      policy: null,
      commentText: '',
      currentUserId: null,
      summarizedContent: null,
    };
  },
  computed: {
    ...mapGetters(['accessToken']),
  },
  created() {
    this.fetchPolicyDetails();
    this.fetchUserId();
  },
  methods: {
    ...mapActions(['clearAccessToken']),
    fetchPolicyDetails() {
      const policyId = this.$route.params.id;
      axios
        .get(`http://localhost:5000/policies/${policyId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.policy = response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch policy details:', error);
        });
    },
    fetchUserId() {
      axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.currentUserId = response.data.id;
        })
        .catch((error) => {
          console.error('Failed to fetch user details:', error);
        });
    },
    getSummary() {
      // Call the function to summarize content
      this.summarizeContent();
    },
    summarizeContent() {
      // Use ChatGPT's API to summarize content
      const prompt = `Summarize the policy: ${this.policy.title}. Content: ${this.policy.content}`;
      axios
        .post('https://api.openai.com/v1/chat/completions', {
          model: 'gpt-3.5-turbo',
          messages: [
            { role: 'system', content: 'You are a helpful assistant.' },
            { role: 'user', content: prompt },
          ],
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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', // Replace with your actual OpenAI API key
          },
        })
        .then((response) => {
          this.summarizedContent = response.data.choices[0].message.content;
        })
        .catch((error) => {
          console.error('Failed to summarize content:', error);
        });
    },
    submitComment(policyId) {
      const accessToken = this.accessToken;

      axios.post(
        `http://localhost:5000/policies/${policyId}/comments`,
        {
          text: this.commentText,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .then((response) => {
        // Refresh policy details after successful comment submission
        this.fetchPolicyDetails();
        this.commentText = ''; // Clear the comment input field
      })
      .catch((error) => {
        console.error('Failed to submit comment:', error);
      });
    },
    deleteComment(commentId) {
      const accessToken = this.accessToken;

      axios
        .delete(`http://localhost:5000/comments/${commentId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          // Refresh policy details after successful comment deletion
          this.fetchPolicyDetails();
        })
        .catch((error) => {
          console.error('Failed to delete comment:', error);
        });
    },
    // ... (existing code)
  },
};
</script>
  
  <style scoped>
  .policy-details-container {
    display: grid;
     /* Adjust the proportions as needed */
    gap: 20px; /* Adjust the gap between sections */
  }

  .policy-details {
    /* Styles for policy details section */
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 8px;
  }

  .comment-section-container {
  /* Styles for comment section container */
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.comment-section {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch; /* Stretch children to take full width */
}

.comment {
  margin-bottom: 10px;
  padding: 8px;
  background-color: #f8f8f8;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%; /* Ensure the form takes full width */
}

.form-group {
  margin-bottom: 10px;
}

.btn-primary {
  margin-top: 10px; /* Add some space between the input and the button */
}


  .user {
    font-weight: bold;
    margin-right: 5px;
  }

  .btn-danger {
    margin-left: 5px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-control {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }

  .btn-primary:hover {
    background-color: #0056b3;
  }
</style>

  