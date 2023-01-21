<template>
  <div class="sign-up-page">
    <h1>Sign Up</h1>
    <form @submit.prevent="submitForm">
      <label>Username:</label>
      <input type="text" name="username" v-model="username"> <br><br>

      <label>First name:</label>
      <input type="text" name="first_name" v-model="first_name"> <br><br>

      <label>Last name:</label>
      <input type="text" name="last_name" v-model="last_name"> <br><br>

      <label>Password:</label>
      <input type="password" name="password" v-model="password"> <br><br>

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>

import axiosInstance from "@/axios";

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      first_name: '',
      last_name: '',
      password: ''
    }
  },
  methods: {
    submitForm(e) {
      const formData = {
        username: this.username,
        first_name: this.username,
        last_name: this.username,
        password: this.password
      }

      axiosInstance
          .post('api/v1/auth/users/', formData)
          .then(response => {
            console.log(response)
            this.$router.push('/log-in')
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>
