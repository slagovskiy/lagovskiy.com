<template>
    <v-container grid-list-md fluid class="pt-0 pb-0 pl-0 pr-0">
        <v-layout row wrap v-if="isAuthenticated">
            <v-flex xs12>
                <v-card>
                    <v-card-title class="headline grey lighten-4">
                        <v-icon left>fa-photo-video</v-icon>
                        Media
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-layout row wrap>
                            <v-flex>

                                <template>
                                    <v-card>
                                        <v-card-title>
                                            <v-btn color="primary" dark class="mb-2">New folder</v-btn>
                                            <v-btn color="primary" dark class="mb-2">Upload photo</v-btn>
                                            <v-btn color="primary" dark class="mb-2" v-bind:loading="loading">Reload
                                            </v-btn>
                                            <v-spacer></v-spacer>
                                        </v-card-title>
                                        <v-layout row wrap>
                                            <v-flex xs12 sm5 md4 lg3 class="pa-2">
                                                <v-list class="elevation-1">
                                                    <v-list-tile @click="selectFolder('')">
                                                        <v-list-tile-action>
                                                            <v-icon>far fa-folder</v-icon>
                                                        </v-list-tile-action>

                                                        <v-list-tile-content>
                                                            sdgsgggs
                                                        </v-list-tile-content>
                                                    </v-list-tile>
                                                </v-list>
                                            </v-flex>
                                            <v-flex xs12 sm7 md8 lg9 class="pa-2">


                                                <v-layout row wrap>
                                                    <v-flex
                                                            v-for="n in 25"
                                                            :key="n"
                                                            xs6
                                                            sm4
                                                            md3
                                                            lg2
                                                            d-flex
                                                    >
                                                        <v-card flat tile class="d-flex">
                                                            <v-img
                                                                    v-bind:src="`https://picsum.photos/500/300?image=${n * 12}`"
                                                                    aspect-ratio="1"
                                                                    class="grey lighten-2"
                                                            >
                                                                <p class="image-btns">
                                                                    <v-btn fab class="image-btn">
                                                                        <v-icon class="image-btn-icon"
                                                                                v-on:click="openImagePreview('https://picsum.photos/1000/700/')">
                                                                            fa-eye
                                                                        </v-icon>
                                                                    </v-btn>
                                                                    <v-btn fab class="image-btn">
                                                                        <v-icon class="image-btn-icon">fa-link</v-icon>
                                                                    </v-btn>
                                                                </p>
                                                                <template v-slot:placeholder>
                                                                    <v-layout
                                                                            fill-height
                                                                            align-center
                                                                            justify-center
                                                                            ma-0
                                                                    >
                                                                        <v-progress-circular
                                                                                indeterminate
                                                                                color="grey lighten-5"
                                                                        ></v-progress-circular>
                                                                    </v-layout>
                                                                </template>
                                                            </v-img>
                                                        </v-card>
                                                    </v-flex>

                                                    <v-dialog
                                                            v-model="dialogPreview"
                                                            persistent
                                                            v-bind:max-height="500"
                                                            v-bind:max-width="700">
                                                        <v-card>
                                                            <v-img
                                                                    v-bind:src="imagePreview"
                                                                    class="grey lighten-2"
                                                                    v-bind:max-height="500"
                                                                    v-bind:max-width="700"

                                                            >
                                                                <template v-slot:placeholder>
                                                                    <v-layout
                                                                            fill-height
                                                                            align-center
                                                                            justify-center
                                                                            ma-0
                                                                    >
                                                                        <v-progress-circular
                                                                                indeterminate
                                                                                color="grey lighten-5"
                                                                        ></v-progress-circular>
                                                                    </v-layout>
                                                                </template>
                                                            </v-img>
                                                            <v-card-actions>
                                                                <v-spacer></v-spacer>
                                                                <v-btn color="" v-on:click="dialogPreview = false">Close
                                                                </v-btn>
                                                            </v-card-actions>
                                                        </v-card>
                                                    </v-dialog>
                                                </v-layout>


                                            </v-flex>
                                        </v-layout>
                                    </v-card>
                                </template>

                            </v-flex>
                        </v-layout>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
        <v-layout row wrap v-else>
            <v-flex xs12>
                <v-alert
                        v-bind:value="true"
                        type="error"
                >Access denied!
                </v-alert>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        name: "Media",
        components: {},
        data() {
            return {
                dialogPreview: false,
                imagePreview: '',
            }
        },
        mounted() {
            //this.loadData()
        },
        created() {
        },
        methods: {
            selectFolder(folder) {
                return folder
            },
            openImagePreview(url) {
                console.log(url)
                this.imagePreview = url
                this.dialogPreview = true
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
            Tag() {
                return this.$store.getters.Tag
            },

        },
        watch: {}
    }
</script>

<style scoped>
    .image-btns {
        text-align: right;
        padding-right: 5px;
    }

    .image-btn {
        width: 25px;
        height: 25px;
        margin-top: 10px;
        margin-left: 1px;
        margin-right: 1px;
        margin-bottom: 0px;
    }

    .image-btn-icon {
        font-size: 12px;
    }
</style>