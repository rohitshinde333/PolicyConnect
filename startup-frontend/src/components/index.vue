<template>
  <div class="home"  >
    <!-- Hero Section -->
    <section class="hero" >
      <div class="hero-content">
        <h1 class="centered-text">
          <span class="letter" style="color: #000000;">P</span>
          <span class="letter" style="color: #000000;">o</span>
          <span class="letter" style="color: #000000;">l</span>
          <span class="letter" style="color: #000000;">i</span>
          <span class="letter" style="color: #000000;">c</span>
          <span class="letter" style="color: #000000;">y</span>
          <span class="letter" style="color: #000000;">C</span>
          <span class="letter" style="color: #000000;">o</span>
          <span class="letter" style="color: #000000;">n</span>
          <span class="letter" style="color: #000000;">n</span>
          <span class="letter" style="color: #000000;">e</span>
          <span class="letter" style="color: #000000;">c</span>
          <span class="letter" style="color: #000000;">t</span>

        </h1>
        <p style="color: rgb(0, 0, 0); font-size: 50px;">
          PolicyConnect aims to revolutionize citizen engagement in the democratic process
        </p>
        
        <button @click="exploreServices" class="btn btn-danger">Explore Services</button>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services" ref="servicesSection" v-show="showServiceSection">
      <div class="container">
        <h1 style="font-size: 50px;">Our Services</h1>
        <vue-carousel :per-page="3" :navigation-enabled="true" :autoplay="true">
          <vue-carousel-slide v-for="(service, index) in services" :key="index">
            <div class="card">
              <img :src="service.icon" :alt="service.title" />
              <h3 style="font-size: 50px;">{{ service.title }}</h3>
              <p style="color:#FF0000">{{ service.description }}</p>
              <p></p>
              <br>
              <p></p>
            </div>
          </vue-carousel-slide>
        </vue-carousel>
      </div>
    </section>

    

   
    
  </div>
</template>

<script>
import VueCarousel from 'vue-carousel';

export default {
  data() {
    return {
      components: {
        VueCarousel,
      },
      services: [
        {
          title: 'Policy Summaries',
          description: 'Get government policies summarized in seconds',
          icon: "https://c0.wallpaperflare.com/preview/148/304/49/judgment-judge-judge-hammer-auction-hammer.jpg",
        },
        {
          title: 'Post your opinion',
          description: 'Share your opinions on policies to the country',
          icon: "https://c0.wallpaperflare.com/preview/121/596/15/opinion-board-blackboard-chalk.jpg",
        },
        {
          title: 'Participate in polls',
          description: 'Support policies you like to see in effect. Government officials are listening',
          icon: "https://c0.wallpaperflare.com/preview/925/223/688/feedback-survey-questionnaire-nps.jpg",
        },
      ],
      showServiceSection: false,
      
    };
  },
  methods: {
    exploreServices() {
      this.showServiceSection = !this.showServiceSection;
      // Get a reference to the services section
      setTimeout(() => {
        // Get a reference to the services section
        const servicesSection = this.$refs.servicesSection;

        // Scroll to the services section with a smooth animation
        servicesSection.scrollIntoView({ behavior: 'smooth' });
      }, 100); 
    },
  },
};
</script>

<style>
/* Hero Section Styles */
.hero {
  background-image: url('https://images.pexels.com/photos/1764702/pexels-photo-1764702.jpeg?auto=compress&cs=tinysrgb&w=600');
  background-size: cover;
  background-position: center;
  color: #ffffff; 
  text-align: center;
  padding: 20px 0px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 3rem;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.centered-text {
  text-align: center;
}

/* Apply different colors to each letter */
.letter {
  display: inline-block;
  font-size: 100px;
}

/* Explore Services Button */
.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.services .card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.services .card {
  /* ... (existing styles) */

  /* Add a transition for a smooth effect */
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

/* Services Section Styles */
.services {
  background-color: #f7f7f7;
  padding: 50px 0;
  
}

.services h2 {
  text-align: center;
  margin-bottom: 40px;
}

/* Additional Content Styles */
.additional-content {
  background-color: #fff;
  padding: 50px 0;
}

.additional-content h2 {
  text-align: center;
  margin-bottom: 40px;
}

.additional-content ul {
  list-style: none;
  padding-left: 0;
}

.additional-content ul li {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

/* Testimonial Styles */
.testimonial {
  margin-bottom: 20px;
}

.testimonial p {
  font-style: italic;
}

.testimonial .author {
  font-weight: bold;
}

/* Add more styles as needed */
</style>
