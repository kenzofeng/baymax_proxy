// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import store from './store'
import VueClipboard from 'vue-clipboard2'
import './before'
import App from './App'
import router from './router'
import '../node_modules/semantic-ui-css/semantic.min.css'
import '../node_modules/semantic-ui-css/semantic.min.js'

Vue.use(VueClipboard)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
