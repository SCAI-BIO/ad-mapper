import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/how-it-works',
    name: 'how-it-works',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/HowItWorksView.vue')
  }, 
  {
    path: "/news",
    name: "news",

    component: () => import('../views/NewsView.vue')
  },
  {
    path: "/upload", 
    name: "upload", 

    component: () => import('../views/UploadView.vue')
  }, 
  {
    path: "/contact", 
    name: "contact", 

    component: () => import('../views/ContactView.vue')
  },
  {
    path: "/cdm",
    name: "cdm",

    component: () => import('../views/CDMTable.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
