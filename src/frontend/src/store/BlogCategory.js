import api from '../common/api'

const initState = {
    Category: {},
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        /*
        setUser(store, payload) {
            store.User = payload.user
            store.isAuthenticated = payload.isAuthenticated
        },
        updateToken(store, token) {
            if (token != '' && token != null) {
                store.jwt = token
                localStorage.setItem('jwt_token', token)
                api.http.defaults.headers.common['Authorization'] = 'JWT ' + this.getters.jwt
            } else {
                localStorage.removeItem('jwt_token')
                api.http.defaults.headers.common['Authorization'] = ''
            }
        }
        */
    },
    actions: {
        /*
        login({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.getToken, payload)
                .then(
                    (response) => {
                        commit('updateToken', response.data.token)
                    })
                .catch((error) => {
                    if (error.response.status === 400) {
                        commit('setError', 'Wrong username or password.')
                        commit('setLoading', false)
                    } else if (error.response.status === 500) {
                        commit('setError', 'Error on server, please, try again later.')
                        commit('setLoading', false)
                    } else {
                        commit('setError', 'Something going wrong. ' + error.response.statusText)
                        commit('setLoading', false)
                    }
                })
        },
        */
    },
    getters: {
        Category(state) {
            return state.Category
        }
    }
}
