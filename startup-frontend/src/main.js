import * as Vue from 'vue'
import router from './router';
import store from './store'
import App from './App.vue';

const app = Vue.createApp(App);

app.use(router);
app.use(store);

app.mount('#app');
