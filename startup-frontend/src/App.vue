<template>
  <div id="app" >
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    
    <nav  id="navbar">
      <ul>
        <li v-if="isAuthenticated">
          <router-link to="/adminHome" v-if="isAdmin"><button class="btn btn-warning">Admin Home</button></router-link> 
          <router-link to="/home" v-else><button class="btn btn-warning">User Home</button></router-link> |
          <router-link to="/about"><button class="btn btn-success">About</button></router-link> |

          <button v-if="isAuthenticated" @click="logout" class="btn btn-danger">Logout</button>
        </li>
        <li v-else>
          <router-link to="/LoginSignUp"><button class="btn btn-danger">Login/SignUp</button></router-link> |
          <router-link to="/about"><button class="btn btn-success">About</button></router-link> |
          <router-link to="/"><button class="btn btn-primary">PolicyConnect</button></router-link> |

        </li>
      </ul>
    </nav>
    
      <router-view style="margin-top: 0px; "></router-view>
      
      
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      isAuthenticated: false,
      prevScrollPos: window.scrollY,
      isNavbarHidden: false,
    };
  },
  computed: {
    ...mapGetters(['isAdmin', 'accessToken','isTheaterAdmin']),
  },
  mounted() {
    this.checkAuthentication();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  watch: {
    accessToken() {
      this.checkAuthentication();
    },
    
  },

  methods: {
    ...mapActions(['clearAccessToken']),
    checkAuthentication() {
      if (this.accessToken) {
        this.isAuthenticated = true;
      } else {
        this.isAuthenticated = false;
      }
    },
    logout() {
        this.clearAccessToken();
        this.$router.push('/');
      },
      handleScroll() {
      const currentScrollY = window.scrollY;

      // Scroll down
      if (this.prevScrollY < currentScrollY) {
        this.isNavbarHidden = true;
      }
      // Scroll up
      else {
        this.isNavbarHidden = false;
      }

      this.prevScrollY = currentScrollY;
    },
  
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: larger;
 
}



/* Navbar Styles */


ul {
  list-style: none;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 0;
  padding: 0;
}

li {
  margin-right: 20px;
}

/* Navigation Link Styles */
router-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

router-link:hover {
  color: #ddd;
}
#navbar {
  top: 0;
  left: 0;
  height: 10%;
  width: 100%;
  background-color: black; /* Facebook's blue color */
  padding: 20px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


/* Logout Button Styles */
.btn-danger {
  background-color: #f02849; /* Facebook's red color */
  color: #fff;
  border: none;
  
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}
.container {
  height: 200vh;
  width: 50vw;
}

.btn-danger:hover {
  background-color: #d4263f;
}

@media (max-width: 768px) {
  /* Styles for screens with a maximum width of 768px (e.g., mobile devices) */
  #navbar {
    height: auto;
    padding: 10px 10px;
    flex-direction: column;
    align-items: center;
  }

  li {
    margin-right: 0;
    margin-bottom: 10px;
  }
}



</style>
