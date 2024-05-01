import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/',
    name: 'Index',
    component: () => import('../components/index.vue')
  },
  {
    path: '/LoginSignUp',
    name: 'LoginSignUp',
    component: () => import('../components/LoginSignup.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/UserHome.vue')
  },
  {
    path: '/AdminHome',
    name: 'AdminHome',
    component: () => import('../components/AdminHome.vue')
  },
  { 
    path: '/policies/:id', 
    component: () => import('../components/PolicyDetails.vue'), 
    name: 'policy-details' 
  },
  { 
    path: '/poll/:id', 
    component: () => import('../components/Poll.vue'), 
    name: 'poll-details' 
  },
  { 
    path: '/user/poll/:id', 
    component: () => import('../components/UserPolls.vue'), 
    name: 'poll' 
  },
  { 
    path: '/qanda', 
    component: () => import('../components/QAPage.vue'), 
    name: 'qanda' 
  },
  { 
    path: '/qa_post', 
    component: () => import('../components/QAPostList.vue'), 
    name: 'qa_post' 
  },
  
]

const router = createRouter({
  base: '/',
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router;
