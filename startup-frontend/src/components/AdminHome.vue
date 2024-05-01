<template>
  <div>
    <div>
      <button v-if="isAuthenticated" @click="delete_my_account" class="btn btn-danger mt-3">Delete My Account</button>

      <button v-if="isAuthenticated" @click="updateProfile()" class="btn btn-warning mt-3" style="margin-left: 50px;">Update Profile</button>

      <div v-if="editingProfile">
        <form @submit="submitProfile" style="margin-left: 70px;">
          <div style="text-align: center; font-size: 20px; margin-bottom: 20px;">Edit Profile</div>
          <div class="form-group">
            <label for="phone" style="font-weight: bold; display: block; margin-bottom: 5px;">Phone:</label>
            <input type="text" v-model="editingProfile.phone" id="phone" class="form-control">
          </div>
          <div class="form-group">
            <label for="email" style="font-weight: bold; display: block; margin-bottom: 5px;">Email:</label>
            <input type="email" v-model="editingProfile.email" id="email" class="form-control">
          </div>
          <div class="form-group">
            <label for="address" style="font-weight: bold; display: block; margin-bottom: 5px;">Address:</label>
            <input type="text" v-model="editingProfile.address" id="address" class="form-control">
          </div>

          <div style="text-align: center; margin-top: 20px;">
            <button type="submit" class="btn btn-success" style="margin-right: 10px;">Save</button>
            <button type="button" @click="cancelEditProfile" class="btn btn-danger">Cancel</button>
          </div>
        </form>
      </div>

      <div>
        <!-- Policies Management Section -->
        <h2 class="mt-3">Manage Policies</h2>
        <button @click="createPolicy" class="btn btn-primary">Create New Policy</button>

        <form v-if="showForm" @submit="submitPolicyForm" style="margin-top: 20px; margin-left: 70px;">
          <h3>{{ formTitle }}</h3>
          <div class="form-group">
            <label for="policyTitle">Title:</label>
            <input type="text" v-model="policyForm.title" id="policyTitle" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="policyContent">Content:</label>
            <textarea v-model="policyForm.content" id="policyContent" class="form-control" rows="3" required></textarea>
          </div>
          <div style="text-align: center; margin-top: 20px;">
            <button type="submit" class="btn btn-success" style="margin-right: 10px;">{{ formAction }}</button>
            <button type="button" @click="cancelPolicyForm" class="btn btn-danger">Cancel</button>
          </div>
        </form>
        <div class="row mt-3">
          <div v-for="policy in policies" :key="policy.id" class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ policy.title }}</h5>
                <p class="card-text">{{ truncateContent(policy.content, 150) }}</p>
                <p class="card-text">Likes: {{ policy.likes }}, Dislikes: {{ policy.dislikes }}</p>
                <div class="btn-group" role="group">
                  <button @click="editPolicy(policy)" class="btn btn-warning">Edit</button>
                  <button @click="deletePolicy(policy.id)" class="btn btn-danger">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
      <div>
        <!-- Polls Management Section -->
        <h2 class="mt-3">Manage Polls</h2>
        <button @click="createPoll" class="btn btn-primary">Create New Poll</button>

        <form v-if="showPollForm" @submit="submitPollForm" style="margin-top: 20px; margin-left: 70px;">
          <h3>{{ pollFormTitle }}</h3>
          <div class="form-group">
            <label for="pollTitle">Title:</label>
            <input type="text" v-model="pollForm.title" id="pollTitle" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="pollDescription">Description:</label>
            <input type="text" v-model="pollForm.description" id="pollDescription" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-success" style="margin-right: 10px;">{{ pollFormAction }}</button>
          <button type="button" @click="cancelPollForm" class="btn btn-danger">Cancel</button>
        </form>

        <!-- Questions and Options Form -->
        <div v-if="selectedPoll">
          <h2 class="mt-3">Add Questions to Poll</h2>
          <button @click="showQuestionsForm = true" class="btn btn-primary">Add New Question</button>

          <form v-if="showQuestionsForm" @submit="submitQuestionsForm" style="margin-top: 20px; margin-left: 70px;">
            <div class="form-group">
              <label for="questionText">Question Text:</label>
              <input type="text" v-model="questionsForm.text" id="questionText" class="form-control" required>
            </div>
            <div style="text-align: center; margin-top: 20px;">
              <button type="submit" class="btn btn-success" style="margin-right: 10px;">Add Question</button>
              <button type="button" @click="cancelQuestionsForm" class="btn btn-danger">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      <div class="row mt-3">
        <div v-for="poll in polls" :key="poll.id" class="col-md-4">
          <div class="card" >
            <div class="card-body">
              <h5 class="card-title" @click="navigateToPollDetails(poll.id)">{{ poll.title }}</h5>
              <p class="card-text" @click="navigateToPollDetails(poll.id)">{{ poll.description }}</p>
              <div class="btn-group" role="group">
                <button @click="editPoll(poll)" class="btn btn-warning">Edit</button>
                <button @click="deletePoll(poll.id)" class="btn btn-danger">Delete</button>
                <!-- Add the following line to call selectPoll when a poll is clicked -->
                <button @click="selectPoll(poll.id)" class="btn btn-primary">Select</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Modal :title="modalTitle" :message="modalMessage" :isOpen="showModal" @close="closeModal" />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  data() {
    return {
      isAuthenticated: false,
      editingProfile: null,
      showModal: false,
      modalTitle: '',
      modalMessage: '',
      userId: 0,
      showForm: false,
      formAction: 'Create Policy',
      formTitle: 'Create New Policy',
      policyForm: {
        title: '',
        content: '',
      },
      policies: [],
      showPollForm: false,
      pollFormAction: 'Create Poll',
      pollFormTitle: 'Create New Poll',
      pollForm: {
        title: '',
      },
      selectedPoll: null,
      showQuestionsForm: false,
      questionsFormAction: 'Add Questions and Options',
      questionsFormTitle: 'Add Questions and Options',
      questionsForm: {
        text: '',
        options: ['Option 1', 'Option 2'], // Initial options
      },
      polls: [],
    };
  },
  computed: {
    ...mapGetters(['accessToken']),
  },
  mounted() {
    this.fetchPolicies();
    this.fetchPolls();
    },
  methods: {
    ...mapActions(['clearAccessToken']),
    truncateContent(content, maxLength) {
      if (content.length <= maxLength) {
        return content;
      } else {
        return content.substring(0, maxLength) + '...';
      }
    },
    

    delete_my_account() {
      axios
        .delete('http://localhost:5000/users', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.$router.push('/');
        })
        .catch((error) => {
          console.error(error);
        });
    },

    fetchUsername() {
      axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.userId = response.data.id;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    fetchPolls() {
      axios.get('http://localhost:5000/polls', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
        this.polls = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navigateToPollDetails(pollId) {
      this.$router.push({ name: 'poll-details', params: { id: pollId } });
    },

    updateProfile() {
      this.editingProfile = {
        phone: '',
        email: '',
        address: '',
      };
    },

    cancelEditProfile() {
      this.editingProfile = null;
    },

    submitProfile(event) {
      event.preventDefault();
      const accessToken = this.accessToken;
      const userId = this.userId;
      axios
        .put(`http://localhost:5000/users/${userId}`, this.editingProfile, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Profile updated successfully';
          this.editingProfile = null;
          this.fetchUsername();
        })
        .catch((error) => {
          console.error('Failed to update profile:', error);
        });
    },

    closeModal() {
      this.showModal = false;
    },

    // Policies Management Section
    createPolicy() {
      this.showForm = true;
      this.formAction = 'Create Policy';
      this.formTitle = 'Create New Policy';
      this.policyForm = {
        title: '',
        content: '',
      };
    },

    editPolicy(policy) {
      this.showForm = true;
      this.formAction = 'Update Policy';
      this.formTitle = 'Edit Policy';
      this.policyForm = {
        title: policy.title,
        content: policy.content,
      };
    },

    cancelPolicyForm() {
      this.showForm = false;
    },

    submitPolicyForm(event) {
      event.preventDefault();
      const accessToken = this.accessToken;

      if (this.formAction === 'Create Policy') {
        
        axios
          .post('http://localhost:5000/policies', this.policyForm, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })
          .then((response) => {
            this.showModal = true;
            this.modalTitle = 'Success';
            this.modalMessage = 'Policy created successfully';
            this.fetchPolicies();
            this.showForm = false;
          })
          .catch((error) => {
            console.error('Failed to create policy:', error);
          });
      } else if (this.formAction === 'Update Policy') {
        // Update existing policy
        // Replace with the actual policy ID you want to update
        const policyId = 1; // Replace with the actual policy ID
        axios
          .put(`http://localhost:5000/policies/${policyId}`, this.policyForm, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })
          .then((response) => {
            this.showModal = true;
            this.modalTitle = 'Success';
            this.modalMessage = 'Policy updated successfully';
            this.fetchPolicies();
            this.showForm = false;
          })
          .catch((error) => {
            console.error('Failed to update policy:', error);
          });
      }
    },

    deletePolicy(policyId) {
      axios
        .delete(`http://localhost:5000/policies/${policyId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Policy deleted successfully';
          this.fetchPolicies();
        })
        .catch((error) => {
          console.error('Failed to delete policy:', error);
        });
    },
    deletePoll(pollId) {
      axios
        .delete(`http://localhost:5000/polls/${pollId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Poll deleted successfully';
          this.fetchPolls();
        })
        .catch((error) => {
          console.error('Failed to delete poll:', error);
        });
    },
    fetchPolicies() {
      axios
        .get('http://localhost:5000/policies', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.policies = response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch policies:', error);
        });
    },
    // Polls Management Section
    createPoll() {
      this.showPollForm = true;
      this.pollFormAction = 'Create Poll';
      this.pollFormTitle = 'Create New Poll';
      this.pollForm = {
        question: '',
        options: '',
      };
    },
    selectPoll(poll) {
      this.selectedPoll = poll;
    },

    submitPollForm(event) {
      event.preventDefault();
      const accessToken = this.accessToken;

      axios
        .post('http://localhost:5000/polls', this.pollForm, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Poll created successfully';
          this.fetchPolicies();
          this.showPollForm = false;
          this.fetchPolls();
        })
        .catch((error) => {
          console.error('Failed to create poll:', error);
        });
    },

    cancelPollForm() {
      this.showPollForm = false;
    },

    // Questions and Options Form
    submitQuestionsForm(event) {
      event.preventDefault();
      const accessToken = this.accessToken;

      // Assume you have the pollId for the current poll (replace with the actual logic to get the pollId)
      const pollId = this.selectedPoll; // Replace with the actual pollId

      axios
        .post(`http://localhost:5000/polls/${pollId}/questions`, this.questionsForm, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Questions and Options added successfully';
          // You may want to reset the form or navigate to another section
          this.showQuestionsForm = false;
          this.questionForm = {
            text: '',
          };
        })
        .catch((error) => {
          console.error('Failed to add questions and options:', error);
        });
    },

    cancelQuestionsForm() {
      this.showQuestionsForm = false;
    },
  },
};
</script>

<style>


.form-group {
  margin: 10px 0;
  padding: 10px;
  width: 900px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

label {
  font-weight: bold;
}

.invalid-feedback {
  color: red;
  margin-top: 5px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.table {
  border-collapse: collapse;
  width: 100%;
  border-color: #000000;
  
}
.th {
  background-color: rgb(224, 182, 126);
}
.td {
  border: 1px solid #000000;
  padding: 8px;
  text-align: left;
  background-color: #ffffff;
}


</style>
