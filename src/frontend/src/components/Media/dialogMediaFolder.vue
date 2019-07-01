<template>
    <v-dialog v-model="dialog" persistent max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                    <v-layout wrap>
                        <v-flex xs12>
                            <v-text-field
                                    v-model="editedItem.name"
                                    label="name"
                            ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field
                                    v-model="editedItem.slug"
                                    label="slug"
                            ></v-text-field>
                        </v-flex>
                        <v-flex xs12>
                            <v-checkbox
                                    v-model="editedItem.deleted"
                                    label="deleted"
                            ></v-checkbox>
                        </v-flex>
                    </v-layout>
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
        name: "dialogMediaFolder",
        data() {
            return {
                formTitle: 'Media Folder',
                /*
                dialog: false,
                editedItem: {
                    id: 0,
                    name: '',
                    slug: '',
                    deleted: false
                },
                */
                defaultItem: {
                    id: -1,
                    name: '',
                    slug: '',
                    deleted: false,
                    created: ''
                }
            }
        },
        methods: {
            close() {
                this.dialog = false
                setTimeout(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                }, 300)
            },
            save() {
                this.$store.dispatch('saveMediaFolder', this.editedItem)
                    .then(() => {
                        if (!this.$store.getters.error)
                            this.close()
                    })
                    .catch(() => {
                    })
            }
        },
        computed: {
            dialog: {
                get: function () {
                    return this.$store.getters.dialogMediaFolder
                },
                set: function(val) {
                    return this.$store.dispatch('setDialogMediaFolder', val)
                }
            },
            editedItem: {
                get: function () {
                    if (this.$store.getters.editedItemMediaFolder === {})
                        return {
                            id: 0,
                            name: '',
                            slug: '',
                            deleted: false,
                            created: ''
                        }
                    else
                        return this.$store.getters.editedItemMediaFolder
                },
                set: function (val) {
                    this.$store.dispatch('setEditedItemMediaFolder', val)
                }
            }
        }
    }
</script>

<style scoped>

</style>