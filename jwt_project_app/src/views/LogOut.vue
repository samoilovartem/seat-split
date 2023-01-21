<template>
  <div class="log-out-page">
    <h1>You just logged out. Bye!</h1>
  </div>
</template>

<script>

import axiosInstance from "@/axios";

export default {
  name: 'LogOut',
  mounted() {
    this.blacklistJwt()
  },
  methods: {
    blacklistJwt(e) {
      axiosInstance
          .post('api/v1/users/blacklist_jwt/', {refresh: localStorage.getItem('refresh')})
          .then(response => {
            console.log(response)
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')
            axiosInstance.defaults.headers.common['Authorization'] = ''
            this.$router.push('/log-in')
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}

</script>
