<template>
  <div class="home">
    <h1>Home</h1>
    <span :src="user_data">Welcome, {{user_data}}</span>
  </div>
</template>

<script>

import axiosInstance from "@/axios";
export default {
  name: 'Home',
  data() {
    return {
      user_data: ''
    }
  },

  mounted() {
    this.getMe()
  },
  methods: {
    getMe(e) {
      axiosInstance
          .get('api/v1/auth/users/me/')
          .then(response => {
            console.log(response)
            this.user_data = response.data.username
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}

</script>
