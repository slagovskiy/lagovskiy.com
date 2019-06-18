<template>
    <v-app>
        <v-navigation-drawer app temporary v-model="drawer">
            <v-list>
                <v-list-tile
                    v-bind:to="this.$router.resolve({name: 'user-profile'}).href"
                >
                    <v-list-tile-action>
                        <v-icon>fa-user</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        {{user.email}}
                    </v-list-tile-content>
                </v-list-tile>
                <template
                    v-for="item in mainMenu"
                >
                    <v-list-tile
                        v-bind:key="item.title"
                        v-bind:to="item.link"
                        v-if="item.auth === isAuthenticated"
                    >
                        <v-list-tile-action>
                            <v-icon>{{item.icon}}</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>{{item.title}}</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app dark color="primary">
            <v-toolbar-side-icon class="hidden-md-and-up"
                                 v-on:click="drawer = !drawer"
            ></v-toolbar-side-icon>
            <v-toolbar-title>
                <router-link to="/" tag="span" class="pointer">
                    <v-icon class="">far fa-smile</v-icon>
                    Application
                </router-link>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items class="hidden-sm-and-down">
                <v-btn flat
                       v-bind:to="this.$router.resolve({name: 'user-profile'}).href"
                       v-if="isAuthenticated"
                >
                    <v-avatar size="36px" class="toolbar-avatar">
                        <img
                            v-if="user.avatar"
                            v-bind:src="this.$config.BASE_URL + user.avatar"
                            v-bind:alt="user.email"
                        >
                    </v-avatar>
                    {{user.email}}
                </v-btn>
                <template
                    v-for="item in mainMenu"
                >
                    <v-btn flat
                           v-bind:key="item.title"
                           v-bind:to="item.link"
                           v-if="item.auth === isAuthenticated"
                    >
                        <v-icon left>{{item.icon}}</v-icon>
                        {{item.title}}
                    </v-btn>
                </template>
            </v-toolbar-items>
        </v-toolbar>
        <v-content>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-content>
        <v-footer app></v-footer>
        <template v-if="error">
            <v-snackbar
                v-bind:timeout="5000"
                v-bind:multi-line="true"
                color="error"
                v-on:input="closeMessages"
                v-bind:value="true"
            >
                {{error}}
                <v-btn flat dark v-on:lick.native="closeMessages">Close</v-btn>
            </v-snackbar>
        </template>
        <template v-if="message">
            <v-snackbar
                v-bind:timeout="5000"
                v-bind:multi-line="true"
                color="primary"
                v-on:input="closeMessages"
                v-bind:value="true"
            >
                {{message}}
                <v-btn flat dark v-on:lick.native="closeMessages">Close</v-btn>
            </v-snackbar>
        </template>
    </v-app>
</template>

<script>
    export default {
        name: 'app',
        created() {

        },
        data() {
            return {
                drawer: false,
                snackbar: false,
                snackbar_text: "",

            }
        },
        components: {},
        methods: {
            closeMessages() {
                this.$store.dispatch('clearMessages')
            },
        },
        computed: {
            mainMenu() {
                return this.$store.getters.mainMenu
            },
            error() {
                return this.$store.getters.error
            },
            message() {
                return this.$store.getters.message
            },
            isAuthenticated() {
                return this.$store.getters.isAuthenticated
            },
            user() {
                return this.$store.getters.user
            }
        }
    }
</script>

<style>
    .pointer {
        cursor: pointer;
    }

    .uppercase {
        text-transform: uppercase;
    }

    .toolbar-text {
        padding-left: 10px;
        padding-right: 10px;
        font-weight: 400;
        font-size: 14px;
        text-transform: uppercase;
    }

    .toolbar-avatar {
        margin-right: 16px;
    }
</style>
