import Vue from 'vue'
import vuetify from '@/plugins/vuetify'
import VuetifyConfirm from 'vuetify-confirm'
import App from './App.vue'
import store from '@/store'
import api from '@/plugins/api'

Vue.config.productionTip = false
Vue.use(api, store)
Vue.use(VuetifyConfirm, { vuetify })

new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
