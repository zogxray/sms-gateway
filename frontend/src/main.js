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
      token: null,
      expired_at: null
    },
    axios: null
  },
  created: function () {
    let self = this
    this.axios = axios.create({
      baseURL: process.env.ROOT_API,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self.auth.token
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
