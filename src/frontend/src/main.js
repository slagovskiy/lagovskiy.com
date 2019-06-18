import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuelidate from 'vuelidate'
import Vuetify from 'vuetify'
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'vuetify/dist/vuetify.min.css'
import '@fortawesome/fontawesome-free/css/all.css'

import App from './App.vue'
import store from './store/index'
import router from './routes'
import config from './common/config'


Vue.use(VueRouter)

Vue.use(Vuetify, {
    iconfont: 'fa',
    theme: {
        "primary": "#546e7a", //"#1976D2",
        "secondary": "#424242",
        "accent": "#82B1FF",
        "error": "#FF5252",
        "info": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FB8C00",

    }
})

Vue.use(Vuelidate)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false
Vue.prototype.$config = config



new Vue({
    render: h => h(App),
    store: store,
    router: router,
    created() {
        router.beforeEach((to, from, next) => {
            if (to.matched.some(record => record.meta.requiresAuth)) {
                if (!this.$store.getters.isAuthenticated) {
                    next({
                        path: this.$router.resolve({name: 'user-login'}).href,
                        query: {redirect: to.fullPath}
                    })
                } else {
                    next()
                }
            } else if (to.matched.some(record => record.meta.requiresNoAuth)) {
                if (this.$store.getters.isAuthenticated) {
                    next({
                        path: this.$router.resolve({name: 'user-profile'}).href
                    })
                } else {
                    next()
                }
            } else {
                next()
            }
        })

        this.$store.dispatch('autoLogin')
    }
}).$mount('#app')
