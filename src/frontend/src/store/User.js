import api from '../common/api'

const initState = {
    User: {},
    isAuthenticated: false,
    jwt: localStorage.getItem('jwt_token'),
}

export default {
    initState: initState,
    state: initState,
    mutations: {
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

    },
    actions: {
        logout({commit}) {
            commit('clearMessages')
            commit('updateToken', '')
            commit('setUser', {'user': {}, 'isAuthenticated': false})
        },
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
        changePassword({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.put(api.userPassword, payload)
                .then(
                    () => {
                        commit('setMessage', 'Password has been successfully changed.')
                        commit('setLoading', false)
                    })
                .catch((error) => {
                    if (error.response.status === 400) {
                        commit('setError', 'Wrong password.')
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
        autoLogin: function ({commit}) {
            commit('clearMessages')
            commit('setLoading', true)
            if (this.getters.jwt != null && this.getters.jwt != '') {
                api.http.defaults.headers.common['Authorization'] = 'JWT ' + this.getters.jwt
                return api.http.get(api.userInfo, {})
                    .then((response) => {
                        commit("setUser",
                            {user: response.data.data[0], isAuthenticated: true}
                        )
                        commit('setLoading', false)
                    })
                    .catch((error) => {
                        commit('updateToken', '')
                        if (error.response.status === 401) {
                            commit('setError', 'Session time out. Please, login again.')
                            commit('setLoading', false)
                        } else if (error.response.status === 500) {
                            commit('setError', 'Error on server, please, try again later.')
                            commit('setLoading', false)
                        } else {
                            commit('setError', 'Something going wrong. ' + error.response.statusText)
                            commit('setLoading', false)
                        }
                    })
            } else {
                commit('setLoading', false)
            }
        },
        registerUser: function({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(
                api.userRegister,
                payload
            )
                .then(() => {
                    commit('setMessage', 'User successfully registered')
                    commit('setLoading', false)
                })
                .catch((error) => {
                    commit('setError', 'User registration failed. ' + error)
                    commit('setLoading', false)
                })
        },
        restorePassword: function({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(
                api.userRestore,
                payload
            )
                .then(() => {
                    commit('setMessage', 'A temporary password has been sent to your email.')
                    commit('setLoading', false)
                })
                .catch(() => {
                    commit('setError', 'Error sending temporary password.')
                    commit('setLoading', false)
                })
        },
        changeUserInfo: function({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.put(
                api.userInfo,
                payload
            )
                .then((response) => {
                    if(response.data.status != 'error') {
                        commit('setMessage', 'User info is updated.')
                        commit('setUser',
                            {user: response.data.data, isAuthenticated: true}
                        )
                    } else {
                        commit('setError', 'Error saving data.')
                    }
                    commit('setLoading', false)
                })
                .catch((error) => {
                    if (error.response.status === 401) {
                        commit('setError', 'Session time out. Please, login again.')
                        commit('setLoading', false)
                    } else if (error.response.status === 500) {
                        commit('setError', 'Error on server, please, try again later.')
                        commit('setLoading', false)
                    } else {
                        commit('setError', 'Something going wrong. ' + error.response.statusText)
                        commit('setLoading', false)
                    }
                })
        }
    },
    getters: {
        isAuthenticated(state) {
            return state.isAuthenticated
        },
        jwt(state) {
            return state.jwt
        },
        user(state) {
            return state.User
        }
    }
}
