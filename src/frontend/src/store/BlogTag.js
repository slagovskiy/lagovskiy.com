import api from '../common/api'

const initState = {
    Tag: []
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setTagList(store, payload) {
            store.Tag = payload
        },
        saveTag(store, payload) {
            let found = false
            for(let i=0; i<store.Tag.length && !found; i++)
            {
                if (store.Tag[i]['id'] === payload['id']) {
                    found = true
                    Object.assign(store.Tag[i], payload)
                }
            }
            if (!found)
                store.Tag.push(payload)
        }
    },
    actions: {
        loadTagList({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.get(api.blogTag, payload)
                .then(
                    (response) => {
                        commit('setTagList', response.data.data)
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error loading data. ' + error)
                    commit('setLoading', false)
                })
        },
        saveTag({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.blogTag, payload)
                .then(
                    (response) => {
                        commit('saveTag', response.data.data)
                        commit('setMessage', 'Saved successfully.')
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error save data. ' + error)
                    commit('setLoading', false)
                })
        }
    },
    getters: {
        Tag(state) {
            return state.Tag
        }
    }
}
