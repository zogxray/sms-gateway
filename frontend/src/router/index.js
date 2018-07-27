import Vue from 'vue'
import Router from 'vue-router'
import Sms from '@/components/Sms'
import Channels from '@/components/Channels'
import AddChannel from '@/components/AddChannel'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Sms',
      component: Sms
    },
    {
      path: '/sms/:page',
      name: 'SmsPage',
      component: Sms
    },
    {
      path: '/channels',
      name: 'Channels',
      component: Channels
    },
    {
      path: '/channels/:page',
      name: 'ChannelsPage',
      component: Channels
    },
    {
      path: '/channels/add',
      name: 'AddChannel',
      component: AddChannel
    }
  ]
})
