<template>
    <v-dialog v-model="show" persistent max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                    <v-form v-model="valid" ref="form" lazy-validation>
                        <v-layout wrap>
                            <v-flex xs12>
                                <v-text-field
                                        label="Select File"
                                        v-on:click='pickFile'
                                        v-model='fileName'
                                        prepend-icon='fa-paperclip'
                                        ref="imageText"
                                ></v-text-field>
                                <input
                                        name="file"
                                        type="file"
                                        style="display: none"
                                        ref="file"
                                        v-on:change="onFilePicked"
                                />
                            </v-flex>
                            <v-flex xs12>
                                <v-select
                                        v-bind:items="mediaFolders"
                                        v-model="item.folder"
                                        item-text="name"
                                        item-value="id"
                                        label="folder"
                                        v-bind:rules="textRules"
                                ></v-select>
                            </v-flex>
                            <v-flex xs12>
                                <v-text-field
                                        v-model="editedItem.name"
                                        label="name"
                                ></v-text-field>
                            </v-flex>
                            <v-flex xs12>
                                <v-text-field
                                        v-model="editedItem.description"
                                        label="description"
                                ></v-text-field>
                            </v-flex>
                            <v-flex xs12>
                                <v-checkbox
                                        v-model="editedItem.deleted"
                                        label="deleted"
                                ></v-checkbox>
                            </v-flex>
                        </v-layout>
                    </v-form>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="" v-on:click="close">Cancel</v-btn>
                <v-btn color="primary" v-on:click="save">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: "dialogMediaFile",
        props: {
            dialog: Boolean,
            item: Object
        },
        data() {
            return {
                formTitle: 'Media File',
                form: new FormData(),
                fileName: '',
                defaultItem: {
                    id: -1,
                    file: '',
                    folder: '',
                    name: '',
                    description: '',
                    deleted: false
                },
                valid: false,
                textRules: [
                    v => !!v || 'Field is required'
                ],
                fileRules: [
                    v => !!v || 'Field is required',
                    v => v.files[0] instanceof File || 'File not selected'
                ]
            }
        },
        methods: {
            pickFile() {
                this.$refs.file.click()
            },
            onFilePicked(e) {
                const files = e.target.files
                if (files[0] !== undefined) {
                    this.fileName = files[0].name
                    if (this.fileName.lastIndexOf('.') <= 0) {
                        return
                    }
                    this.form.append('file', this.$refs.file.files[0])
                    this.form.append('filename', this.fileName)
                } else {
                    this.fileName = ''
                }
            },
            deleteItem(item) {
                if (confirm('Are you sure you want to delete this item?')) {
                    this.editedItem = Object.assign({}, item)
                    this.editedItem.deleted = true
                    this.$store.dispatch('saveCategory', this.editedItem)
                }
            },
            restoreItem(item) {
                if (confirm('Are you sure you want to restore this item?')) {
                    this.editedItem = Object.assign({}, item)
                    this.editedItem.deleted = false
                    this.$store.dispatch('saveMediaFile', this.editedItem)
                }
            },
            close() {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.form = new FormData()
                this.fileName = ''
                this.show = false
            },
            save() {
                if(this.$refs.form.validate()) {
                    for (let prop in this.editedItem) {
                        if (this.editedItem.hasOwnProperty(prop)) {
                            this.form.append(prop, this.editedItem[prop])
                        }
                    }
                    this.$store.dispatch('saveMediaFile', this.form)
                        .then(() => {
                            if (!this.$store.getters.error)
                                this.close()
                        })
                        .catch(() => {
                        })
                }
            }
        },
        computed: {
            show: {
                get() {
                    return this.dialog
                },
                set(value) {
                    this.$emit('close', value)
                }
            },
            editedItem: {
                get: function () {
                    if (Object.entries(this.item).length === 0 && this.item.constructor === Object)
                        return {
                            id: -1,
                            file: '',
                            folder: '',
                            name: '',
                            description: '',
                            deleted: false
                        }
                    else
                        return this.item
                },
                set: function (value) {
                    this.$emit('clear', value)
                }
            },
            mediaFolders: {
                get: function () {
                    return this.$store.getters.MediaFolder
                },
                set: function () {
                }
            }
        }
    }
</script>

<style scoped>

</style>