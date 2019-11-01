<template>
    <v-container grid-list-md fluid class="pt-0 pb-0 pl-0 pr-0">
        <v-layout v-if="isAuthenticated">
            <v-flex xs12>
                <v-card>
                    <v-card-title class="headline grey lighten-4">
                        <v-icon left>far fa-user</v-icon>
                        User profile
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-layout row wrap>
                            <v-flex xs12 sm5 md4 lg3>
                                <v-card flat>
                                    <template v-if="user.avatar">
                                        <v-img
                                                v-bind:src="user.url"
                                                height="200px"
                                                contain
                                        ></v-img>
                                    </template>
                                    <v-card-actions>
                                        <v-spacer/>
                                        <v-btn color="primary" v-on:click="dialogAvatar = true">Change avatar</v-btn>
                                        <v-spacer/>
                                    </v-card-actions>
                                </v-card>

                            </v-flex>
                            <v-flex xs12 sm7 md8 lg9>
                                <v-card flat>
                                    <v-card-title primary-title>
                                        <h1 class="uppercase">{{user.email}}</h1>
                                    </v-card-title>
                                    <v-card-text class="">
                                        <p class="title">First name: <span
                                                class="font-weight-light">{{user.firstname}}</span>
                                        </p>
                                        <p class="title">Last name: <span
                                                class="font-weight-light">{{user.lastname}}</span>
                                        </p>
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-btn
                                                color="primary"
                                                v-on:click="loadUser"
                                        >change info
                                        </v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-flex>
                        </v-layout>
                    </v-card-text>
                </v-card>
            </v-flex>
            <!-- DIALOGS -->
            <template>
                <v-dialog v-model="dialogAvatar" persistent max-width="350">
                    <v-form ref="formAvatar" enctype="multipart/form-data">
                        <v-card>
                            <v-card-title class="headline">Select image</v-card-title>
                            <v-card-text class="text-md-center">
                                <img
                                        v-bind:src="imageUrl"
                                        height="200px"
                                        v-if="imageUrl"
                                />
                                <v-text-field
                                        label="Select Image"
                                        v-on:click='pickFile'
                                        v-model='imageName'
                                        prepend-icon='fa-paperclip'
                                        ref="imageText"
                                ></v-text-field>
                                <input
                                        name="file"
                                        type="file"
                                        style="display: none"
                                        ref="image"
                                        accept="image/*"
                                        v-on:change="onFilePicked"
                                />
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="" v-on:click="dialogAvatar = false">Cancel</v-btn>
                                <v-btn
                                        color="primary"
                                        v-on:click.prevent="uploadAvatar"
                                        v-bind:loading="loading"
                                >Upload
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-form>
                </v-dialog>
                <v-dialog v-model="dialogInfo" persistent max-width="350">
                    <v-form v-model="validInfo" ref="formInfo">
                        <v-card>
                            <v-card-title class="headline">User info</v-card-title>
                            <v-card-text class="text-md-center">
                                <v-text-field
                                        label="First name"
                                        v-model="userFirstname"
                                        ref="userFirstname"
                                ></v-text-field>
                                <v-text-field
                                        label="Last name"
                                        v-model="userLastname"
                                        ref="userLastname"
                                ></v-text-field>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer/>
                                <v-btn color="" v-on:click="dialogInfo = false">Cancel</v-btn>
                                <v-btn
                                        color="primary"
                                        v-on:click.prevent="saveUser"
                                        v-bind:loading="loading"
                                >Save
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-form>
                </v-dialog>
            </template>
        </v-layout>
        <v-layout v-else>
            <v-flex xs12>
                <v-alert
                        v-bind:value="true"
                        type="error"
                >
                    Access denied!
                </v-alert>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import api from '../../common/api'

    function initialState() {
        // Object.assign(this.$data, initialState());
        return {
            dialogAvatar: false,
            dialogInfo: false,
            validInfo: false,
            form: new FormData(),
            imageName: '',
            imageUrl: '',
            imageFile: '',
            userFirstname: '',
            userLastname: '',
        }
    }

    export default {
        name: "User",
        data() {
            return initialState()
        },
        methods: {
            pickFile() {
                this.$refs.image.click()
            },

            onFilePicked(e) {
                const files = e.target.files
                if (files[0] !== undefined) {
                    this.imageName = files[0].name
                    if (this.imageName.lastIndexOf('.') <= 0) {
                        return
                    }
                    const fr = new FileReader()
                    fr.readAsDataURL(files[0])
                    fr.addEventListener('load', () => {
                        this.imageUrl = fr.result
                        this.imageFile = files[0]
                        this.form.append('file', this.$refs.image.files[0])
                        this.form.append('filename', this.imageName)
                    })
                } else {
                    this.imageName = ''
                    this.imageFile = ''
                    this.imageUrl = ''
                }
            },
            uploadAvatar() {
                this.$store.dispatch('setLoading', true)
                if (this.$refs.image.files[0] instanceof File) {
                    api.http.post(api.userAvatar,
                        this.form,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                    )
                        .then((response) => {
                            if (response.data.status == 'ok') {
                                Object.assign(this.$data, initialState())
                                this.$store.dispatch('autoLogin')
                                    .then(() => {
                                        this.$store.dispatch('setMessage', 'Avatar is updated.')
                                        this.dialogInfo = false
                                    })
                            }
                        })
                        .catch((error) => {
                            this.$store.dispatch('setError', 'Data transfer error. ' + error)
                        })
                        .finally(() => {

                        })
                } else {
                    this.$store.dispatch('setError', 'File not selected.')
                }
                this.$store.dispatch('setLoading', false)
            },
            loadUser() {
                this.userFirstname = this.user.firstname
                this.userLastname = this.user.lastname
                this.dialogInfo = true
            },
            saveUser() {
                this.$store.dispatch('changeUserInfo', {
                    'firstname': this.userFirstname,
                    'lastname': this.userLastname
                })
                    .then(() => {
                        this.dialogInfo = false
                    })
                    .catch(() => {
                    })
            }
        },
        computed: {
            isAuthenticated() {
                return this.$store.getters.isAuthenticated
            },
            user() {
                return this.$store.getters.user
            },
            loading() {
                return this.$store.getters.loading
            },
            adminMenu() {
                return this.$store.getters.adminMenu
            }
        }

    }
</script>

<style scoped>
</style>
