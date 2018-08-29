// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router/index'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css' // This line here
import axios from 'axios'
import moment from 'moment-timezone'
import vueMoment from 'vue-moment'
require('moment/locale/ru')

Vue.config.productionTip = false
Vue.use(VueMaterial)
Vue.use(vueMoment, {
  moment
})

Vue.component('pagination', require('laravel-vue-pagination'))

export const trans = new Vue({
  data: {
    translation: {}
  }
})

Vue.prototype.$axios = axios.create({
  baseURL: process.env.ROOT_API,
  headers: {
    'Content-Type': 'application/json'
  }
})

Vue.filter('trans', function (value) {
  if (!value && trans.translation[value]) {
    return ''
  }

  return trans.translation[value]
})

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>',
  data: {
    auth: {
      token: null
    }
  },
  watch: {
    auth: {
      handler: function () {
        if (this.auth.token !== null) {
          localStorage.setItem('token', this.auth.token)
        }

        this.$axios.defaults.headers['Authorization'] = 'Bearer ' + this.auth.token
      },
      deep: true
    }
  },
  created: function () {
    let self = this

    let token = localStorage.getItem('token')

    if (token !== null) {
      self.auth.token = token
      self.$axios.defaults.headers['Authorization'] = 'Bearer ' + this.auth.token
    }

    self.$axios.interceptors.response.use(function (response) {
      return response
    }, function (error) {
      if (error.response.status === 401) {
        self.auth.token = null
        localStorage.removeItem('token')
        self.$router.push({name: 'Login'})
      } else {
        return Promise.reject(error)
      }
    })
  }
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login') {
    if (app.$data.auth.token !== null) {
      next()
    } else {
      next({name: 'Login'})
    }
  } else {
    next()
  }
})
