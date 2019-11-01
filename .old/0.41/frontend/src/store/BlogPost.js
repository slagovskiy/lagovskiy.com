import api from '../common/api'

const initState = {
    Post: [],
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setPostList(store, payload) {
            store.Post = payload
        },
        savePost(store, payload) {
            let found = false
            for (let i = 0; i < store.Post.length && !found; i++) {
                if (store.Post[i]['id'] === payload['id']) {
                    found = true
                    Object.assign(store.Post[i], payload)
                }
            }
            if (!found)
                store.Post.push(payload)
        },
    },
    actions: {
        loadPostList({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.get(api.blogPost, payload)
                .then(
                    (response) => {
                        commit('setPostList', response.data.data)
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error loading data. ' + error)
                    commit('setLoading', false)
                })
        },
        savePost({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.blogPost, payload)
                .then(
                    (response) => {
                        commit('savePost', response.data.data)
                        commit('setMessage', 'Saved successfully.')
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error save data. ' + error)
                    commit('setLoading', false)
                })
        },
    },
    getters: {
        Post(state) {
            return state.Post
        },
    }
}
