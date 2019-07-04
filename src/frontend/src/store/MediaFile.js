import api from '../common/api'

const initState = {
    MediaFile: [],
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setMediaFileList(store, payload) {
            store.MediaFile = payload
        },
        saveMediaFile(store, payload) {
            let found = false
            for (let i = 0; i < store.MediaFile.length && !found; i++) {
                if (store.MediaFile[i]['id'] === payload['id']) {
                    found = true
                    Object.assign(store.MediaFile[i], payload)
                }
            }
            if (!found)
                store.MediaFile.push(payload)
        },
    },
    actions: {
        loadMediaFileList({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.get(api.mediaFile, payload)
                .then(
                    (response) => {
                        commit('setMediaFileList', response.data.data)
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error loading data. ' + error)
                    commit('setLoading', false)
                })
        },
        saveMediaFile({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.mediaFile, payload)
                .then(
                    (response) => {
                        commit('saveMediaFile', response.data.data)
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
        MediaFile(state) {
            return state.MediaFile
        },
    }
}
