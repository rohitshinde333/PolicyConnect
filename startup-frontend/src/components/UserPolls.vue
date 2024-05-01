<template>
    <div class="active-polls-container">
      <h2>Active Polls</h2>
      
      <div>
        <div class="poll-card" v-if="Poll">
          <h3>{{ Poll.title }}</h3>
          <p>{{ Poll.description }}</p>
          <div>
            <div v-for="question in Poll.questions" :key="question.id" class="poll-question">
              <h4>{{ question.text }}</h4>
              <ul>
                <li v-for="option in question.options" :key="option.id">
                  <input
                    type="radio"
                    :id="`option_${option.id}`"
                    :value="option.id"
                    v-model="selectedOptions[question.id]"
                  />
                  <label :for="`option_${option.id}`">{{ option.text }} : {{ option.votes }}</label>
                </li>
              </ul>
            </div>
            <button @click="vote(Poll)">Vote</button>
          </div>
          
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters, mapActions } from 'vuex';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        Poll: null, // Assuming you have a Vuex getter named 'activePolls'
        selectedOptions: {}, // Track the selected options for each question
      };
    },
  
    computed: {
      ...mapGetters(['accessToken']),
    },
  
    mounted() {
      this.fetchActivePolls();
    },
  
    methods: {
      ...mapActions(['clearAccessToken', 'fetchUserDetails']), // Adjust actions accordingly
  
      async fetchActivePolls() {
        try {
          const pollId = this.$route.params.id;

          const response = await axios.get(`http://localhost:5000/polls/${pollId}`, {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          });
          this.Poll = response.data;
        } catch (error) {
          console.error('Failed to fetch active polls:', error);
        }
      },
  
      
  
      async vote(poll) {
  const selectedOptions = { ...this.selectedOptions };

  // Validate that the user has selected an option for each question
  for (const question of poll.questions) {
    const selectedOptionId = selectedOptions[question.id]; // Move the declaration inside the loop
    if (!selectedOptionId) {
      alert('Please select an option for each question.');
      return;
    }

    try {
      // Submit the vote
      await axios.put(`http://localhost:5000/options/${selectedOptionId}` );

      // Refresh the user details (e.g., check if the user has voted)
      

      alert('Vote recorded successfully!');
      // Reset the selected options
      this.selectedOptions = {};
      // Refresh the active polls
      this.fetchActivePolls();
    } catch (error) {
      console.error('Failed to submit vote:', error);
    }
  }
},
    },
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  .poll-card {
    border: 1px solid #ccc;
    padding: 15px;
    margin: 10px 0;
  }
  
  .poll-question {
    margin-bottom: 15px;
    margin-right: 400px;
  }
  
  input[type="radio"] {
    margin-right: 5px;
  }
  </style>
  