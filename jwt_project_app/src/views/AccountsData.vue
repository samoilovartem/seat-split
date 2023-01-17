<template>
  <vuetable ref="vuetable"
    api-url="http://127.0.0.1:8000/api/v1/accounts/"
    :fields="['first_name', 'last_name', 'email']"
    data-path="results"
    pagination-path="next"
  ></vuetable>
</template>

<script>
import Vuetable from 'vuetable-2'

export default {
  components: {
    Vuetable
  }
}
</script>