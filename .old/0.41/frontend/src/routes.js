import VueRouter from 'vue-router'
import Home from './views/Home'
import User from './views/User/User'
import Login from './views/User/Login'
import Logout from './views/User/Logout'
import Register from './views/User/Register'
import ChangePassword from './views/User/ChangePassword'
import RestorePassword from './views/User/RestorePassword'
import BlogCategory from './views/Blog/Category'
import BlogTag from './views/Blog/Tag'
import BlogPost from './views/Blog/Post'
import BlogPostEdit from './views/Blog/PostEdit'
import Media from './views/Media/MediaFolder'
import Error404 from './views/Error'


export default new VueRouter({
    routes: [
        {
            path: '/',
            component: Home,
            name: 'home'
        },

        {
            path: '/user/profile',
            component: User,
            name: 'user-profile',
            meta: {requiresAuth: true}
        },
        {
            path: '/user/login',
            component: Login,
            name: 'user-login',
            meta: {requiresNoAuth: true}
        },
        {
            path: '/user/logout',
            component: Logout,
            name: 'user-logout',
            meta: {requiresAuth: true}
        },
        {
            path: '/user/register',
            component: Register,
            name: 'user-register',
            meta: {requiresNoAuth: true}
        },
        {
            path: '/user/password',
            component: ChangePassword,
            name: 'user-password',
            meta: {requiresAuth: true}
        },
        {
            path: '/user/restore',
            component: RestorePassword,
            name: 'user-restore',
            meta: {requiresNoAuth: true}
        },

        {
            path: '/blog/category',
            component: BlogCategory,
            name: 'blog-category',
            meta: {requiresAuth: true}
        },
        {
            path: '/blog/tag',
            component: BlogTag,
            name: 'blog-tag',
            meta: {requiresAuth: true}
        },
        {
            path: '/blog/post',
            component: BlogPost,
            name: 'blog-post',
            meta: {requiresAuth: true}
        },
        {
            path: '/blog/post/:id',
            component: BlogPostEdit,
            name: 'blog-post-edit',
            props: true,
            meta: {requiresAuth: true}
        },
        {
            path: '/media',
            component: Media,
            name: 'media',
            meta: {requiresAuth: true}
        },

        {
            path: '*',
            component: Error404
        }
    ],
    mode: 'history',
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return {selector: to.hash}
        }
        return {
            x: 0,
            y: 0
        }
    }
})
