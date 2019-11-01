<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Registration form</v-toolbar-title>
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
                            <v-text-field
                                    id="confirmPassword" prepend-icon="fa-lock" name="confirmPassword" label="Confirm Password" type="password"
                                    v-model="confirmPassword"
                                    v-bind:counter="6"
                                    v-bind:rules="confirmPasswordRules"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary"
                            v-on:click.prevent="onSubmit"
                            v-bind:disabled="!valid"
                            v-bind:loading="loading"
                        >Register</v-btn>
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
        name: "Register",
        data() {
            return {
                valid: false,
                email: 'sergey@lagovskiy.com',
                password: '121212',
                confirmPassword: '121212',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => reEmail.test(v) || 'E-mail must be valid'
                ],
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length >= 6) || 'Password must be equal or more than 6 characters'
                ],
                confirmPasswordRules: [
                    v => !!v || 'Password is required',
                    v => v === this.password || 'Password should match'
                ]
            }
        },
        methods: {
            onSubmit() {
                if (this.$refs.form.validate()) {
                    const user = {
                        email: this.email,
                        password: this.password
                    }
                    this.$store.dispatch('registerUser', user)
                        .then(() => {
                            if(!this.$store.getters.error)
                                this.$router.push({name: 'user-login'})
                        })
                        .catch(() => {})
                        .finally(() => {})
                }
            }
        },
        computed: {
            loading() {
                return this.$store.getters.loading
            }
        }

    }
</script>

<style scoped>

</style>
