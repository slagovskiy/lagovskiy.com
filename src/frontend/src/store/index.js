import Vue from 'vue'
import Vuex from 'vuex'
import Menu from './Menu'
import User from './User'
import Global from './Global'
import blogCategory from './BlogCategory'
import blogTag from './BlogTag'
import Media from './Media'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        menu: Menu,
        user: User,
        blogCategory: blogCategory,
        blogTag: blogTag,
        media: Media,
        global: Global
    },
    state: {},
    getters: {},
    mutations: {},
    actions: {}
})
