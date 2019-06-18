<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Restore password form</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form v-model="valid" ref="form" lazy-validation>
                            <p>Enter your email address to get a temporary password.</p>
                            <v-text-field
                                    id="email" prepend-icon="fa-user" name="email" label="Email" type="text"
                                    v-model="email"
                                    v-bind:rules="emailRules"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" v-on:click.prevent="onSubmit" v-bind:disabled="!valid" v-bind:loading="loading">Restore</v-btn>
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
        name: "RestorePassword",
        data() {
            return {
                valid: false,
                email: '',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => reEmail.test(v) || 'E-mail must be valid'
                ],
            }
        },
        methods: {
            onSubmit() {
                if (this.$refs.form.validate()) {
                    const user = {
                        email: this.email
                    };
                    this.$store.dispatch('restorePassword', user)
                        .then(() => {
                            if(!this.$store.getters.error)
                            {
                                this.$router.push({name: 'user-login'})
                            }
                        })
                        .catch(() => {})
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
