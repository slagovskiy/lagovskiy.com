import api from '../common/api'

const initState = {
    Category: [],
    dialogBlogCategory: false,
    editedItemBlogCategory: {},
}

export default {
    initState: initState,
    state: initState,
    mutations: {
        setCategoryList(store, payload) {
            store.Category = payload
        },
        saveCategory(store, payload) {
            let found = false
            for (let i = 0; i < store.Category.length && !found; i++) {
                if (store.Category[i]['id'] === payload['id']) {
                    found = true
                    Object.assign(store.Category[i], payload)
                }
            }
            if (!found)
                store.Category.push(payload)
        },
        setDialogBlogCategory(state, payload) {
            state.dialogBlogCategory = payload
        },
        setEditedItemBlogCategory(state, payload) {
            state.editedItemBlogCategory = payload
        },
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
        },
        saveCategory({commit}, payload) {
            commit('clearMessages')
            commit('setLoading', true)
            return api.http.post(api.blogCategory, payload)
                .then(
                    (response) => {
                        commit('saveCategory', response.data.data)
                        commit('setMessage', 'Saved successfully.')
                        commit('setLoading', false)
                    }
                )
                .catch((error) => {
                    commit('setError', 'Error save data. ' + error)
                    commit('setLoading', false)
                })
        },
        setDialogBlogCategory({commit}, payload) {
            commit('setDialogBlogCategory', payload)
        },
        setEditedItemBlogCategory({commit}, payload) {
            commit('setEditedItemBlogCategory', payload)
        },
    },
    getters: {
        Category(state) {
            return state.Category
        },
        dialogBlogCategory(state) {
            return state.dialogBlogCategory
        },
        editedItemBlogCategory(state) {
            return state.editedItemBlogCategory
        },
    }
}
