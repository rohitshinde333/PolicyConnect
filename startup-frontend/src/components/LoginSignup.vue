<template>
  <div class="login-container">
    <div class="form-container" style="margin-top: -100px;">
      <div class="tabs">
        <button
          @click="toggleForm('login')"
          :class="{ active: showLogin }"
          class="tab"
        >
          Login
        </button>
        <button
          @click="toggleForm('signup')"
          :class="{ active: showSignup }"
          class="tab"
        >
          Signup
        </button>
      </div>
      <div class="form">
        <form @submit="login" v-if="showLogin">
          <div class="input-group">
            <label for="username">Username</label>
            <input
              type="text"
              id="username"
              v-model="loginData.name"
              placeholder="Username"
            />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="loginData.password"
              placeholder="Password"
            />
          </div>
          
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <form @submit="signup" v-if="showSignup" >
          <div class="input-group-horizontal">
          <div class="input-group">
            <label for="signup-username">Username</label>
            <input
              type="text"
              id="signup-username"
              v-model="signupData.name"
              placeholder="Username"
            />
          </div>
          <div class="input-group">
            <label for="signup-username">Password</label>
            <input type="password" v-model="signupData.password" placeholder="Password" required>
          </div>
          </div>
          <div class="input-group-horizontal">

          <div class="input-group">
            <label for="signup-username">Email</label>
            <input type="text" v-model="signupData.email" placeholder="Email" required>
          </div>
          <div class="input-group">
            <label for="signup-username">Address</label>
            <select v-model="signupData.address" required style="width:100%; margin-top: -35px;">
              <option disabled value="">Select a city</option>
              <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
            </select>
          </div>
          </div>
          <div class="input-group-horizontal">

          <div class="input-group">
            <label for="signup-username">Phone</label>
            <input type="text" v-model="signupData.phone" placeholder="Phone" required>
          </div>
          <div class="input-group">

          <div class="admin-checkbox">
            <label for="admin">Admin:</label>
            <input type="checkbox" v-model="signupData.is_admin" id="admin">
          </div>
          <div class="input-group">
            <input type="password" v-if="signupData.is_admin" v-model="signupData.key" placeholder="Enter Admin Verification">
          </div>
          </div>
        </div>
          <button type="submit" class="btn btn-success">Signup</button>
          
        </form>
      </div>
    </div>
    <loading-spinner v-if="isLoading" />
  </div>
</template>

<script>
import axios from 'axios';
import AdminHome from './AdminHome.vue';
import UserHome from './UserHome.vue';
import LoadingSpinner from './LoadingSpinner.vue';

export default {
  components: {
    AdminHome,
    UserHome,
    LoadingSpinner,
  },
  data() {
    return {
      isLoading: false,
      showLogin: false,
      showSignup: false,
      loginData: {
        name: '',
        password: '',
      },
      signupData: {
        name: '',
        password: '',
        email: '',
        address: '',
        phone: '',
        is_admin: false,
        key: '',
      },
      cities: [
      
        { id: 1, name: 'Mumbai' },
        { id: 2, name: 'Delhi' },
        { id: 3, name: 'Bangalore' },
        { id: 4, name: 'Chennai' },
        { id: 5, name: 'Kolkata' },
        { id: 6, name: 'Hyderabad' },
        { id: 7, name: 'Pune' },
        { id: 8, name: 'Ahmedabad' },
        { id: 9, name: 'Jaipur' },
        { id: 10, name: 'Lucknow' },
        { id: 11, name: 'Kanpur' },
        { id: 12, name: 'Nagpur' },
        { id: 13, name: 'Indore' },
        { id: 14, name: 'Chandigarh' },
        { id: 15, name: 'Coimbatore' },
        { id: 16, name: 'Kochi' },
        { id: 17, name: 'Bhopal' },
        { id: 18, name: 'Vadodara' },
        { id: 19, name: 'Visakhapatnam' },
        { id: 20, name: 'Surat' },
        { id: 21, name: 'Patna' },
        { id: 22, name: 'Ludhiana' },
        { id: 23, name: 'Agra' },
        { id: 24, name: 'Varanasi' },
        { id: 25, name: 'Sangli' },
        { id: 26, name: 'Chhatrapati Sambhajinagar' },
        { id: 27, name: 'Nanded' },
        { id: 28, name: 'Parbhani' }
      ],
      isAuthenticated: false,
      isAdmin: false,
      isTheatreAdmin: false,
    };
  },
  mounted()  {
    this.toggleForm('login');
  },
  methods: {
    toggleForm(form) {
      if (form === 'login') {
        this.showLogin = true;
        this.showSignup = false;
      } else if (form === 'signup') {
        this.showLogin = false;
        this.showSignup = true;
      } 
    },
    login(event) {
      event.preventDefault();
      this.isLoading = true;
      // Make API request to login endpoint
      axios 
        .post('http://localhost:5000/login', this.loginData)
        .then(response => {
          // Handle successful login
          console.log('Logged in successfully');

          this.isAuthenticated = true;
          this.isAdmin = response.data.is_admin;
          this.isTheatreAdmin = response.data.is_theatre_admin;
          this.$store.dispatch('setAccessToken', {
            token: response.data.access_token
            
          });

          this.$store.dispatch('setIsAdmin', {
            is_admin: response.data.is_admin
            
          });

          this.$store.dispatch('setIsTheaterAdmin',{
            is_theater_admin: response.data.is_theatre_admin

          })
          this.$store.dispatch('setTheatreId',{
            theatre_id: response.data.theatre_id
          })

          if (this.isAdmin) {
            this.$router.push('/AdminHome');
          } else if (this.isTheatreAdmin) {
            this.$router.push('/TheatreAdminHome');
          } else {
            this.$router.push('/home')
          };
          this.isLoading = false;
        })
        .catch(error => {
          // Handle login error
          alert(error.response.data.message);
          console.error('Login failed:', error.response.data.message);
          this.loginData.name = '';
          this.loginData.password = '';
        });
    },

    async signup(event) {
      event.preventDefault();
      this.isLoading = true;
      // Make API request to signup endpoint
      axios
        .post('http://localhost:5000/users', this.signupData)
        .then(response => {
          // Handle successful signup
          alert(response.data.message);
          console.log('Signed up successfully');
          this.sendEmail();
          this.isLoading = false;
        })
        .catch(error => {
          // Handle signup error
          console.error('Signup failed:', error);
          alert("Something went wrong. Email ID in use")
        });
    },
    async sendEmail() {
      const emailData = {
        recipient: this.signupData.email,
        subject: "welcome / do-not reply",
        body: "Hello user, Welcome to PolicyConnect. This is an autogenerated mail. Please do not reply to this mail. Thank you!!!",
      };

      axios({
        method: 'post',
        url: 'http://localhost:5000/email',
        data: emailData,
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => {
          console.log('Email sent:', response.data.message);
        })
        .catch(error => {
          console.error('Failed to send email:', error);
        });
    },
    
  },
};
</script>


<style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .form-container {
    width: 500px;
    background-color: #fff;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 20px;
  }

  .tabs {
    display: flex;
    margin-bottom: 20px;
  }

  .tab {
    flex: 1;
    padding: 10px;
    cursor: pointer;
    border: none;
    background-color: #f5f5f5;
    border-radius: 5px 5px 0 0;
    color: #333;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }

  .tab.active {
    background-color: #1877f2;
    color: #fff;
  }

  .form {
    display: flex;
    flex-direction: column;
  }

  .input-group {
    margin-bottom: 15px;
  }

  label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }

  input,
  select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
    margin-top: 5px;
  }

  .btn {
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }

  .btn-primary {
    background-color: #1877f2;
    color: #fff;
  }

  .btn-success {
    background-color: #28a745;
    color: #fff;
  }

  .input-group-horizontal {
    display: flex;
    margin-bottom: 15px;
  }

  .input-group-horizontal .input-group {
    flex: 1;
    margin-right: 10px;
  }

  .admin-checkbox {
    display: flex;
    align-items: center;
  }

  .admin-checkbox label {
    margin-right: 10px;
  }

  .admin-checkbox input {
    margin-top: 5px;
  }

  .admin-checkbox {
    display: flex;
    align-items: center;
  }

  .admin-checkbox label {
    margin-right: 10px;
  }

  .admin-checkbox input {
    margin-top: 5px;
  }

  .loading-spinner {
    text-align: center;
    margin-top: 20px;
  }

  @media (max-width: 768px) {
    .form-container {
      width: 100%;
    }
  }
</style>
