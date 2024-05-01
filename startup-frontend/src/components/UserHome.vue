<template>
  <div>
    <div class="page-container">
      <p v-if="isAuthenticated">Logged in as: {{ username }}</p>
      <p v-else>Please log in to see your username.</p>
      <div class="buttons-container">
        <button v-if="isAuthenticated" @click="deleteMyAccount" class="btn btn-danger" style="margin-left: 270px;">Delete Account</button>
        <button v-if="isAuthenticated" @click="updateProfile" class="btn btn-warning" style="position: relative; margin-left: 50px;">Update Profile</button>
        <button v-if="isAuthenticated" @click="navigateToQandA" class="btn btn-warning" style="position: relative; margin-left: 50px;">Q and A</button>

      </div>
      <div v-if="editingProfile" class="profile-form">
          <h2 style="color: #333; font-family: 'Arial', sans-serif; text-align: center;">Edit Profile</h2>
          <div style="margin-bottom: 10px;">
              <label for="phone" style="font-weight: bold; display: block; margin-bottom: 5px;">Phone:</label>
              <input type="text" v-model="editingProfile.phone" id="phone" class="form-control" style="width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;">
          </div>
          <div style="margin-bottom: 10px;">
              <label for="email" style="font-weight: bold; display: block; margin-bottom: 5px;">Email:</label>
              <input type="email" v-model="editingProfile.email" id="email" class="form-control" style="width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;">
          </div>
          <div style="margin-bottom: 10px;">
              <label for="address" style="font-weight: bold; display: block; margin-bottom: 5px;">Address:</label>
              <input type="text" v-model="editingProfile.address" id="address" class="form-control" style="width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;">
          </div>
          <div class="form-buttons" style="text-align: center;">
              <button type="submit" class="btn btn-success" style="margin-left: 400px;">Save</button>
              <button type="button" @click="cancelEditProfile" class="btn btn-danger">Cancel</button>
          </div>
      </div>

      <br>
      <Modal :title="modalTitle" :message="modalMessage" :isOpen="showModal" @close="closeModal" />
    </div>
    <div class="search-container">
      <div class="search-inputs">
        <label for="searchQuery">Search policy</label>
        <input type="text" v-model="searchQuery" id="searchQuery" @input="performSearch" placeholder="Mining policy 2023">
      </div>
      <div v-for="policy in queryResults" :key="policy.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title" @click="navigateToPolicyDetails(policy.id)" >{{ policy.title }}</h5>
            <p class="card-text" @click="navigateToPolicyDetails(policy.id)" >{{ truncateContent(policy.content, 150) }}</p>
            <p class="card-text" >Likes: {{ policy.likes }}</p>
            <div class="btn-group" role="group" >
              <button @click="likePolicy(policy.id)" class="btn btn-success">Like</button>
            </div>
          </div>  
        </div>
      </div>
    </div>
    <div>
      <h1>Policies</h1>
    </div>
    <div class="row mt-3">
      <div v-for="policy in policies" :key="policy.id" class="col-md-4">
        <div class="card" >
          <div class="card-body">
            <h5 class="card-title" @click="navigateToPolicyDetails(policy.id)">{{ policy.title }}</h5>
            <p class="card-text" @click="navigateToPolicyDetails(policy.id)">{{ truncateContent(policy.content, 150) }}</p>
            <p class="card-text">Likes: {{ policy.likes }}</p>
            <div class="btn-group" role="group">
              <button @click="likePolicy(policy.id)" class="btn btn-success">Like</button>
            </div>
          </div>  
        </div>
      </div>
    </div>
    <div>
      <h1>Polls</h1>
    </div>
    <div class="row mt-3">
        <div v-for="poll in polls" :key="poll.id" class="col-md-4">
          <div class="card" >
            <div class="card-body">
              <h5 class="card-title" @click="navigateToPoll(poll.id)">{{ poll.title }}</h5>
              <p class="card-text" @click="navigateToPoll(poll.id)">{{ poll.description }}</p>
            </div>
          </div>
        </div>
      </div>
  </div>
  
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import axios from 'axios';
import Modal from './Modal.vue';
import { useStore } from 'vuex';


export default {
  components: {
    Modal,
    
  },
  data() {
    return {
      isAuthenticated: false,
      editingProfile: null,
      username: '',
      userId: 0,
      message: '',
      showModal: false,
      selectedServiceType: 'freelancer', // Initialize the selected service type
      queryResults: [],
      searchQuery: 'mining policy 2022',
      policies: [],
      polls: [],
      commentText: '',
    };
  },
  
  computed: {
    ...mapGetters(['accessToken']),
  },
  mounted() {
    this.fetchUsername();
    this.performSearch();
    this.fetchPolicies();
    this.fetchPolls();
  },
  methods: {
    ...mapActions(['clearAccessToken']),
    async performSearch() {
      if (this.searchQuery === '') {
        this.queryResults = [];
        return;
      }

      // Make an API request to perform the search based on the selected service type
      const accessToken = this.accessToken;

      
      await axios
        .get(`http://localhost:5000/search-policies?policy_name=${this.searchQuery}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
            withCredentials: true,
          })
          .then((response) => {
            this.queryResults = response.data;
          })
          .catch((error) => {
            console.error('Failed to perform search:', error);
          });
      
      
    },
    navigateToQandA() {
      this.$router.push({name:'qanda'})
    },
    navigateToPoll(pollId) {
      this.$router.push({ name:'poll', params: { id: pollId}})
    },
    navigateToPolicyDetails(policyId) {
      this.$router.push({ name: 'policy-details', params: { id: policyId } });
    },
    truncateContent(content, maxLength) {
      if (content.length <= maxLength) {
        return content;
      } else {
        return content.substring(0, maxLength) + '...';
      }
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
    deleteMyAccount() {
      axios
        .delete('http://localhost:5000/users', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Handle account deletion response...
        })
        .catch((error) => {
          console.error(error);
        });
    },
    
    fetchUsername() {
      const store = useStore();
      const accessToken = store.getters.accessToken;
      axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          // Handle the response from the protected resource
          this.isAuthenticated = true;
          this.message = response.data.message;
          this.username = response.data.name;
          this.userId = response.data.id;
        })
        .catch((error) => {
          // Handle the error
          console.error(error);
        });
    },
    
    logout() {
      // Clear the access token from the store and perform any other necessary logout actions
      this.clearAccessToken();
      // Redirect the user to the login page or any other desired page
      this.$router.push('/');
    },
    
    updateProfile(event) {
      event.preventDefault();
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
          // Handling the successful profile update
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Profile updated successfully';

          // Reseting the editingProfile and fetch the updated profile data
          this.editingProfile = null;
          this.fetchUsername();
        })
        .catch((error) => {
          // Handling the profile update error
          console.error('Failed to update profile:', error);
        });
    },
    
    closeModal() {
      this.showModal = false;
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
    likePolicy(policyId) {
      // Send a request to like the policy
      axios
        .put(`http://localhost:5000/policies/${policyId}/like`, null, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Refresh the policy data after a successful like
          this.fetchPolicies();
        })
        .catch((error) => {
          console.error('Failed to like policy:', error);
        });
    },

    
  },
};
</script>



<style scoped>
.page-container {
  padding: 20px;
  background-color: #f5f6f7;
  border: 1px solid #ccc;
  border-radius: 5px;
  
}

h1 {
  font-size: 28px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.buttons-container {
  display: flex;
  align-items: center;
  gap: 10px;
  
}

.btn {
  padding: 10px 20px;
  border-radius: 5px;
}

.btn-danger {
  background-color: #f02849;
  color: #fff;
  border: none;
}

.btn-danger:hover {
  background-color: #d8122d;
}

.btn-warning {
  background-color: #f0a820;
  color: #fff;
  border: none;
}

.btn-warning:hover {
  background-color: #d88f18;
}

.profile-form {
  margin: 20px 0;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.form-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-success {
  background-color: #20b366;
  color: #fff;
  border: none;
}

.btn-success:hover {
  background-color: #188c4f;
}

.search-container {
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 20px;
}

.search-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

label {
  font-weight: bold;
}

select, input[type="text"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .page-container, .search-container {
    padding: 10px;
  }

  .btn {
    padding: 8px 16px;
    font-size: 14px;
  }

  h1 {
    font-size: 24px;
  }

  h2 {
    font-size: 20px;
  }

  select, input[type="text"] {
    padding: 8px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 20px;
  }

  h2 {
    font-size: 18px;
  }

  .btn {
    padding: 6px 12px;
    font-size: 12px;
  }

  select, input[type="text"] {
    padding: 6px;
    font-size: 12px;
  }
}
</style>