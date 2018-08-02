import Vue from 'vue'
import Router from 'vue-router'
import IncomingSms from '@/components/IncomingSms'
import OutgoingSms from '@/components/OutgoingSms'
import SendSms from '@/components/SendSms'
import Channels from '@/components/Channels'
import AddChannel from '@/components/AddChannel'
import Ussd from '@/components/Ussd'
import SendUssd from '@/components/SendUssd'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'IncomingSms',
      component: IncomingSms
    },
    {
      path: '/incoming-sms/:page',
      name: 'IncomingSmsPage',
      component: IncomingSms
    },
    {
      path: '/outgoing-sms',
      name: 'OutgoingSms',
      component: OutgoingSms
    },
    {
      path: '/outgoing-sms/:page',
      name: 'OutgoingSmsPage',
      component: OutgoingSms
    },
    {
      path: '/outgoing-sms/add',
      name: 'SendSms',
      component: SendSms
    },
    {
      path: '/ussd',
      name: 'Ussd',
      component: Ussd
    },
    {
      path: '/ussd/:page',
      name: 'UssdPage',
      component: Ussd
    },
    {
      path: '/ussd/add',
      name: 'SendUssd',
      component: SendUssd
    },
    {
      path: '/',
      name: 'Ussd',
      component: Ussd
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
    },
    {
      path: '/channels/:id/edit',
      name: 'EditChannel',
      component: AddChannel
    }
  ]
})
