export default {
    state: {
        loading: false,
        error: null,
        message: null,
        dialog: false,
        editedItem: {}
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
            state.message = null
            state.error = null
        },
        setDialog(state, payload) {
            state.dialog = payload
        },
        setEditedItem(state, payload) {
            state.editedItem = payload
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
        },
        setDialog({commit}, payload) {
            commit('setDialog', payload)
        },
        setEditedItem({commit}, payload) {
            commit('setEditedItem', payload)
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
        },
        dialog(state) {
            return state.dialog
        },
        editedItem(state) {
            return state.editedItem
        }
    }
}

