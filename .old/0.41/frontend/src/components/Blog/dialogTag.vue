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
                                        v-model="editedItem.name"
                                        label="name"
                                        v-bind:rules="textRules"
                                ></v-text-field>
                            </v-flex>
                            <v-flex xs12>
                                <v-text-field
                                        v-model="editedItem.slug"
                                        label="slug"
                                        v-bind:rules="textRules"
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
        name: "dialogTag",
        props: {
            dialog: Boolean,
            item: Object
        },
        data() {
            return {
                formTitle: 'Tag',
                defaultItem: {
                    id: -1,
                    name: '',
                    slug: '',
                    deleted: false
                },
                valid: false,
                textRules: [
                    v => !!v || 'Field is required'
                ],
            }
        },
        methods: {
            close() {
                //this.editedItem = Object.assign({}, this.defaultItem)
                this.show = false
            },
            save() {
                if(this.$refs.form.validate()) {
                    this.$store.dispatch('saveTag', this.editedItem)
                        .then((response) => {
                            if (!this.$store.getters.error){
                                this.editedItem = Object.assign({}, response.data.data)
                                this.close()
                            }
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
                            name: '',
                            slug: '',
                            deleted: false
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