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
                                            <v-btn color="primary" dark class="mb-2" v-on:click="addNewMediaFolder">New
                                                folder
                                            </v-btn>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="addNewMediaFile">Upload
                                                photo
                                            </v-btn>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="loadData"
                                                   v-bind:loading="loading">Reload
                                            </v-btn>
                                            <v-spacer></v-spacer>
                                        </v-card-title>
                                        <v-layout row wrap>
                                            <v-flex xs12 sm5 md4 lg3 class="pa-2">
                                                <v-list class="elevation-1">
                                                    <template v-for="item in MediaFolder">
                                                        <v-list-tile
                                                                v-bind:key="item.id"
                                                                v-on:click="selectFolder(item.id)"
                                                        >
                                                            <v-list-tile-content>
                                                                {{item.name}}
                                                            </v-list-tile-content>
                                                            <v-list-tile-action>
                                                                <v-icon
                                                                        small
                                                                        class="mr-2"
                                                                        v-on:click="editMediaFolderItem(item)"
                                                                >
                                                                    fa-pencil-alt
                                                                </v-icon>
                                                            </v-list-tile-action>
                                                            <v-list-tile-action>
                                                                <template v-if="item.deleted">
                                                                    <v-icon
                                                                            small
                                                                            v-on:click="deleteMediaFolderItem(item)"
                                                                    >
                                                                        fa-trash-restore-alt
                                                                    </v-icon>
                                                                </template>
                                                                <template v-else>
                                                                    <v-icon
                                                                            small
                                                                            v-on:click="deleteMediaFolderItem(item)"
                                                                    >
                                                                        fa-trash-alt
                                                                    </v-icon>
                                                                </template>
                                                            </v-list-tile-action>
                                                        </v-list-tile>
                                                    </template>
                                                </v-list>
                                                <app-dialog-media-folder
                                                        v-bind:dialog="dialogMediaFolder"
                                                        v-bind:item="editedMediaFolder"
                                                        v-on:close="dialogMediaFolder = $event"
                                                        v-on:clear="editedMediaFolder = $event"
                                                ></app-dialog-media-folder>
                                            </v-flex>

                                            <v-flex xs12 sm7 md8 lg9 class="pa-2">


                                                <v-layout row wrap>
                                                    <v-flex
                                                            v-for="item in MediaFile"
                                                            :key="item.id"
                                                            xs6 sm4 md3 lg2 d-flex
                                                    >
                                                        <v-card flat tile class="d-flex">
                                                            <v-img
                                                                    v-bind:src="item.url"
                                                                    aspect-ratio="1"
                                                                    class="grey lighten-2"
                                                            >
                                                                <p class="image-btns">
                                                                    <v-btn fab class="image-btn">
                                                                        <v-icon class="image-btn-icon"
                                                                                v-on:click="openImagePreview(item.url)">
                                                                            fa-eye
                                                                        </v-icon>
                                                                    </v-btn>
                                                                    <v-btn fab class="image-btn">
                                                                        <v-icon class="image-btn-icon">fa-link</v-icon>
                                                                    </v-btn>
                                                                </p>
                                                                <template v-slot:placeholder>
                                                                    <v-layout
                                                                            fill-height align-center justify-center ma-0
                                                                    >
                                                                        <v-progress-circular indeterminate
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
                                                                    height="auto"
                                                                    width="auto"
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

                                                <app-dialog-media-file
                                                        v-bind:dialog="dialogMediaFile"
                                                        v-bind:item="editedMediaFile"
                                                        v-on:close="dialogMediaFile = $event"
                                                        v-on:clear="editedMediaFile = $event"
                                                ></app-dialog-media-file>

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
    import DialogMediaFolder from '../../components/Media/dialogMediaFolder'
    import DialogMediaFile from '../../components/Media/dialogMediaFile'

    export default {
        name: "Media",
        components: {
            appDialogMediaFolder: DialogMediaFolder,
            appDialogMediaFile: DialogMediaFile,
        },
        data() {
            return {
                dialogMediaFolder: false,
                editedMediaFolder: {},
                dialogMediaFile: false,
                editedMediaFile: {},
                dialogPreview: false,
                imagePreview: '',
            }
        },
        mounted() {
            this.loadData()
        },
        created() {
        },
        methods: {
            loadData() {
                this.$store.dispatch('loadMediaFolderList', {})
                this.$store.dispatch('loadMediaFileList', {})
            },
            selectFolder(folder) {
                return folder
            },
            openImagePreview(url) {
                this.imagePreview = url
                this.dialogPreview = true
            },
            editMediaFolderItem(item) {
                this.editedMediaFolder = Object.assign({}, item)
                this.dialogMediaFolder = true
            },
            deleteMediaFolderItem(item) {
                item.deleted = !item.deleted
                this.$store.dispatch('saveMediaFolder', item)
            },
            addNewMediaFolder() {
                this.dialogMediaFolder = true
            },
            addNewMediaFile() {
                this.dialogMediaFile = true
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
            MediaFolder() {
                return this.$store.getters.MediaFolder
            },
            MediaFile() {
                return this.$store.getters.MediaFile
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

    .v-list__tile__action {
        min-width: 0px;
    }
</style>