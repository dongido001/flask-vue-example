import 'es6-promise/auto'

import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import axios from 'axios'

import {routes, publicPages}  from './routes'
import stores from './store/'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.prototype.$http = axios;

const router = new VueRouter({ routes })
const store = new Vuex.Store(stores)

router.beforeEach((to, from, next) => {
  if (!publicPages.includes(to.path)) {
    if ( !(localStorage.getItem('token') && localStorage.getItem('logged_user_email')) ){
      localStorage.removeItem('token')
      localStorage.removeItem('logged_user_email')
      return next('/login')
    }
  }

  next()
})


new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
