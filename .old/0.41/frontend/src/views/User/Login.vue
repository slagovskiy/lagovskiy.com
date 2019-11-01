<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Login form</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form v-model="valid" ref="form" lazy-validation>
                            <v-text-field
                                id="email" prepend-icon="fa-user" name="email" label="Email" type="text"
                                v-model="email"
                                v-bind:rules="emailRules"
                            ></v-text-field>
                            <v-text-field
                                id="password" prepend-icon="fa-lock" name="password" label="Password" type="password"
                                v-model="password"
                                v-bind:counter="6"
                                v-bind:rules="passwordRules"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="primary" v-on:click="restorePassword">Forgot your password?</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary"
                               v-on:click.prevent="onSubmit"
                               v-bind:disabled="!valid"
                               v-bind:loading="loading"
                        >Login
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    // eslint-disable-next-line
    var reEmail = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

    export default {
        name: "Login",
        data() {
            return {
                valid: false,
                email: 'slagovskiy@gmail.com',
                password: '123qwe',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => reEmail.test(v) || 'E-mail must be valid'
                ],
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length >= 6) || 'Password must be equal or more than 6 characters'
                ]
            }
        },
        computed: {
            isAuthenticated(state) {
                return state.isAuthenticated
            },
            loading() {
                return this.$store.getters.loading
            }
        },
        methods: {
            onSubmit() {
                if (this.$refs.form.validate()) {
                    var user = {
                        'email': this.email,
                        'password': this.password
                    }
                    this.$store.dispatch('login', user)
                        .then(() => {
                            if (this.$store.getters.jwt) {
                                this.$store.dispatch('autoLogin')
                                    .then(() => {
                                        if(this.$route.query['redirect'])
                                            this.$router.push(this.$route.query['redirect'])
                                        else
                                            this.$router.push({name: 'user-profile'})
                                    })
                            }
                        })
                        .catch(() => {
                        });
                }
            },
            restorePassword() {
                this.$router.push({name: 'user-restore'});
            }
        }
    }
</script>

<style scoped>

</style>
