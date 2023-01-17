import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from "@/views/SignUp.vue";
import LogIn from "@/views/LogIn.vue";
import LogOut from "@/views/LogOut.vue";
import AccountsData from "@/views/AccountsData.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/accounts',
    name: 'Accounts Data',
    component: AccountsData
  },
  {
    path: '/about',
    name: 'about',

    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/log-out',
    name: 'LogOut',
    component: LogOut
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
