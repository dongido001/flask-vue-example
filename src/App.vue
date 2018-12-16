<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script>
import { EventBus } from '../Event'

export default {
  name: 'App',
  data () {
    return {
      authenticated: false,
      email: null,
    }
  },
  methods: {
    setAuthenticated(access_token, email) {
      localStorage.auth = access_token
      this.authenticated = true
      this.email = email
    },
    mounted() {
      try {   
          this.token = localStorage.getItem('b_token')
      } catch(e) { }
    }
  }
}
</script>
