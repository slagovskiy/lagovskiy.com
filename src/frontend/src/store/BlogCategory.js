import api from '../common/api'

const initState = {
    Category: []
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setCategoryList(store, payload) {
            store.Category = payload
        }
    },
    actions: {
        loadCategoryList({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.get(api.blogCategory, payload)
                .then(
                    (response) => {
                        commit('setCategoryList', response.data.data)
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error loading data. ' + error)
                    commit('setLoading', false)
                })
        }
    },
    getters: {
        Category(state) {
            return state.Category
        }
    }
}
