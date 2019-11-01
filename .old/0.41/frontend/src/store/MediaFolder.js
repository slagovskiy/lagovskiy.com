import api from '../common/api'

const initState = {
    MediaFolder: [],
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setMediaFolderList(store, payload) {
            store.MediaFolder = payload
        },
        saveMediaFolder(store, payload) {
            let found = false
            for (let i = 0; i < store.MediaFolder.length && !found; i++) {
                if (store.MediaFolder[i]['id'] === payload['id']) {
                    found = true
                    Object.assign(store.MediaFolder[i], payload)
                }
            }
            if (!found)
                store.MediaFolder.push(payload)
        },
    },
    actions: {
        loadMediaFolderList({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.get(api.mediaFolder, payload)
                .then(
                    (response) => {
                        commit('setMediaFolderList', response.data.data)
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error loading data. ' + error)
                    commit('setLoading', false)
                })
        },
        saveMediaFolder({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.mediaFolder, payload)
                .then(
                    (response) => {
                        commit('saveMediaFolder', response.data.data)
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
        MediaFolder(state) {
            return state.MediaFolder
        },
    }
}
