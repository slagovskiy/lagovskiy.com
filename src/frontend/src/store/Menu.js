import router from '../routes'

export default {
    state: {
        mainMenu: [
            {
                icon: 'fa-sign-in-alt',
                title: 'Login',
                link: router.resolve({name: 'user-login'}).href,
                auth: false
            },
            {
                icon: 'fa-user',
                title: 'Registration',
                link: router.resolve({name: 'user-register'}).href,
                auth: false
            },
            {
                icon: 'fa-key',
                title: 'Change password',
                link: router.resolve({name: 'user-password'}).href,
                auth: true
            },
            {
                icon: 'fa-sign-out-alt',
                title: 'Logout',
                link: router.resolve({name: 'user-logout'}).href,
                auth: true
            },
        ],
        adminMenu: [
            {
                icon: 'far fa-folder',
                title: 'Categories',
                link: router.resolve({name: 'blog-category'}).href,
                auth: true
            },
            {
                icon: 'fa-tag',
                title: 'Tags',
                link: router.resolve({name: 'blog-tag'}).href,
                auth: true
            },
            {
                icon: 'fa-edit',
                title: 'Posts',
                link: '/blog/post/',
                auth: true
            },
        ]
    },
    getters: {
        mainMenu(state) {
            return state.mainMenu
        },
        adminMenu(state) {
            return state.adminMenu
        }
    }
}
