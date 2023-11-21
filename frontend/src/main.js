import Vue from 'vue'
import App from './App.vue'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import './assets/css/node_attrs_detail_table.css'
import './assets/css/index.css'

Vue.use(ElementUI, { locale })

Vue.config.productionTip = false

import * as d3 from "d3"
window.d3 = d3

import * as $ from 'jquery'
window.$ = $

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
