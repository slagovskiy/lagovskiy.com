<template>
    <v-dialog v-model="show" persistent max-width="500px">
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
        props: {
            dialog: Boolean,
            item: Object,
        },
        data() {
            return {
                formTitle: 'Media Folder',
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
                this.show = false
                this.editedItem = Object.assign({}, this.defaultItem)
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
            show: {
                get: function () {
                    return this.dialog
                },
                set: function(value) {
                    this.$emit('close', value)
                }
            },
            editedItem: {
                get: function () {
                    if (this.item === {})
                        return {
                            id: 0,
                            name: '',
                            slug: '',
                            deleted: false,
                            created: ''
                        }
                    else
                        return this.item
                },
                set: function (value) {
                    this.$emit('clear', value)
                }
            }
        }
    }
</script>

<style scoped>

</style>