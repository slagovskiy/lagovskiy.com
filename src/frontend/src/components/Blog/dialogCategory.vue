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
                            <v-text-field
                                    v-model="editedItem.order"
                                    label="order"
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
        name: "dialogCategory",
        data() {
            return {
                formTitle: 'Category',
                /*
                dialog: false,
                editedItem: {
                    id: 0,
                    name: '',
                    slug: '',
                    order: 10,
                    deleted: false
                },
                */
                defaultItem: {
                    id: -1,
                    name: '',
                    slug: '',
                    order: 10,
                    deleted: false
                }
            }
        },
        methods: {
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
                    this.$store.dispatch('saveCategory', this.editedItem)
                }
            },
            close() {
                this.dialog = false
                setTimeout(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                }, 300)
            },
            save() {
                this.$store.dispatch('saveCategory', this.editedItem)
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
                    return this.$store.getters.dialogBlogCategory
                },
                set: function(val) {
                    return this.$store.dispatch('setDialogBlogCategory', val)
                }
            },
            editedItem: {
                get: function () {
                    if (this.$store.getters.editedItemBlogCategory === {})
                        return {
                            id: 0,
                            name: '',
                            slug: '',
                            order: 10,
                            deleted: false
                        }
                    else
                        return this.$store.getters.editedItemBlogCategory
                },
                set: function (val) {
                    this.$store.dispatch('setEditedItemBlogCategory', val)
                }
            }
        }
    }
</script>

<style scoped>

</style>