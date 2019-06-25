<template>
    <v-container grid-list-md fluid class="pt-0 pb-0 pl-0 pr-0">
        <v-layout row wrap v-if="isAuthenticated">
            <v-flex xs12>
                <v-card>
                    <v-card-title class="headline grey lighten-4">
                        <v-icon left>far fa-folder</v-icon>
                        Categories
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-layout row wrap>
                            <v-flex>

                                <template>
                                    <v-card>
                                        <v-card-title>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="dialog=true">New Item</v-btn>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="loadData" v-bind:loading="loading">Reload</v-btn>
                                            <v-spacer></v-spacer>
                                            <v-text-field
                                                    v-model="search"
                                                    append-icon="fa-search"
                                                    label="Search"
                                                    single-line
                                                    hide-details
                                                    v-on:input="searchData"
                                            ></v-text-field>
                                        </v-card-title>
                                        <v-data-table
                                                v-bind:items="filteredData"
                                                v-bind:headers="headers"
                                                v-bind:pagination.sync="pagination"
                                                v-bind:loading="loading"
                                                prev-icon="fa-caret-left"
                                                next-icon="fa-caret-right"
                                                sort-icon="fa-arrow-up v-icon-table"
                                                class="elevation-1"
                                        >
                                            <template v-slot:items="props">
                                                <td class="text-xs-left">{{ props.item.name }}</td>
                                                <td class="text-xs-left">{{ props.item.slug }}</td>
                                                <td class="text-xs-center">{{ props.item.order }}</td>
                                                <td class="text-xs-center">
                                                    <template v-if="props.item.deleted">
                                                        <v-icon small>fa-trash-alt</v-icon>
                                                    </template>
                                                </td>
                                                <td class="text-xs-center">
                                                    <v-icon
                                                            small
                                                            class="mr-2"
                                                            v-on:click="editItem(props.item)"
                                                    >
                                                        fa-pencil-alt
                                                    </v-icon>
                                                    <template v-if="props.item.deleted">
                                                        <v-icon
                                                                small
                                                                v-on:click="restoreItem(props.item)"
                                                        >
                                                            fa-trash-restore-alt
                                                        </v-icon>
                                                    </template>
                                                    <template v-else>
                                                        <v-icon
                                                                small
                                                                v-on:click="deleteItem(props.item)"
                                                        >
                                                            fa-trash-alt
                                                        </v-icon>
                                                    </template>
                                                </td>
                                            </template>
                                            <template v-slot:no-data>
                                                Sorry, nothing to display here :(
                                            </template>
                                        </v-data-table>
                                    </v-card>
                                </template>

                                <v-dialog v-model="dialog" max-width="500px">
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
                >Access denied!</v-alert>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import debounce from 'debounce'

    export default {
        name: "Category",
        data() {
            return {
                pagination: {
                    sortBy: 'name',
                    rowsPerPage: 25 // -1 for All",
                },
                search: '',
                filteredData: [],
                headers: [
                    {text: 'name', align: 'center', sortable: true, value: 'name'},
                    {text: 'slug', align: 'center', sortable: true, value: 'slug'},
                    {text: 'order', align: 'center', sortable: true, value: 'order'},
                    {text: 'deleted', align: 'center', sortable: true, value: 'deleted'},
                    {text: 'action', align: 'center', sortable: false},
                ],

                dialog: false,
                formTitle: 'Category',
                editedIndex: -1,
                editedItem: {
                    name: '',
                    slug: '',
                    order: 10,
                    deleted: false
                },
                defaultItem: {
                    name: '',
                    slug: '',
                    order: 10,
                    deleted: false
                }
            }
        },
        mounted() {
            this.loadData()
        },
        created() {
            this.searchData = debounce(this.searchData, 1000)
        },
        methods: {
            loadData() {
                this.$store.dispatch('loadCategoryList', {})
                    .then(() => {
                        this.filteredData = this.Category
                    })
            },
            searchData() {
                if (this.search == '') {
                    this.filteredData = this.Category
                } else {
                    this.filteredData = []
                    for (let i = 0; i < this.Category.length; i++) {
                        let s = ''
                        for (let key in this.Category[i]) {
                            if (typeof (this.Category[i][key]) != 'boolean')
                                s += this.Category[i][key].toString()
                        }
                        if (s.includes(this.search))
                            this.filteredData.push(this.Category[i])
                    }
                }
            },
            editItem(item) {
                this.editedItem = Object.assign({}, item)
                this.dialog = true
            },
            deleteItem(item) {
                const index = item.id
                confirm('Are you sure you want to delete this item?') && this.filteredData.splice(index, 1)
            },
            restoreItem(item) {
                const index = item.id
                confirm('Are you sure you want to delete this item?') && this.filteredData.splice(index, 1)
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
                        this.close()
                    })
                    .catch(() => {})
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
            Category() {
                return this.$store.getters.Category
            },

        },
        watch: {}
    }
</script>

<style scoped>

</style>