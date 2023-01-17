<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/accounts">Accounts Data</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/sign-up">Sign Up</router-link> |
    <router-link to="/log-in">Log In</router-link> |
    <router-link to="/log-out">Log Out</router-link>
  </nav>
  <router-view/>
</template>

<script>

import axiosInstance from "@/axios";

export default {
  name: 'App',
  beforeCreate() {
    this.$store.commit('initializeStore')

    const access = this.$store.state.access

    if (access) {
      axiosInstance.defaults.headers.common['Authorization'] = `JWT ${access}`
    } else {
      axiosInstance.defaults.headers.common['Authorization'] = ''
    }
  },
}


</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
