export default {
    state: {
        loading: false,
        error: null,
        message: null
    },
    mutations: {
        setLoading(state, payload) {
            state.loading = payload
        },
        setError(state, payload) {
            state.error = payload
        },
        setMessage(state, payload) {
            state.message = payload
        },
        clearMessages(state) {
            state.error = null
        }
    },
    actions: {
        setLoading({commit}, payload) {
            commit('setLoading', payload)
        },
        setError({commit}, payload) {
            commit('setError', payload)
        },
        setMessage({commit}, payload) {
            commit('setMessage', payload)
        },
        clearMessages({commit}) {
            commit('clearMessages')
        }
    },
    getters: {
        loading(state) {
            return state.loading
        },
        error(state) {
            return state.error
        },
        message(state) {
            return state.message
        }
    }
}

