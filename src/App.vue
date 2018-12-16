<template>
  <v-app>
    <Dashboard v-if="authenticated" :email="email"/>
    <Login
       v-else 
       v-on:authenticated="setAuthenticated"
    />
  </v-app>
</template>

<script>
import { EventBus } from '../Event'
import Twilio, { connect, createLocalTracks, createLocalVideoTrack } from 'twilio-video'
import axios from 'axios'

import Dashboard from './components/Dashboard'
import Login from './components/Login'

export default {
  name: 'App',
  components: {
    Dashboard,
    Login
  },
  data () {
    return {
      authenticated: false,
      email: null,
    }
  },
  props: ['username'],
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
