// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
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

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>',
  data: {
    axios: axios.create({
      baseURL: process.env.ROOT_API
    })
  }
})
