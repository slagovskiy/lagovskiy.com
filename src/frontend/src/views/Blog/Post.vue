<template>
    <v-container grid-list-md fluid class="pt-0 pb-0 pl-0 pr-0">
        <v-layout row wrap v-if="isAuthenticated">
            <v-flex xs12>
                <v-card>
                    <v-card-title class="headline grey lighten-4">
                        <v-icon left>fa-edit</v-icon>
                        Posts
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-layout row wrap>
                            <v-flex>

                                <template>
                                    <v-card>
                                        <v-card-title>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="addNem">New Item
                                            </v-btn>
                                            <v-btn color="primary" dark class="mb-2" v-on:click="loadData"
                                                   v-bind:loading="loading">Reload
                                            </v-btn>
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
                                                <td class="text-xs-left">{{ props.item.title }}</td>
                                                <td class="text-xs-left">{{ postStatus(props.item.status) }}</td>
                                                <td class="text-xs-center">{{ props.item.created | moment("from", "now")
                                                    }}
                                                </td>
                                                <td class="text-xs-center">
                                                    <v-icon
                                                            small
                                                            class="mr-2"
                                                            v-on:click="editItem(props.item)"
                                                    >
                                                        fa-pencil-alt
                                                    </v-icon>
                                                </td>
                                            </template>
                                            <template v-slot:no-data>
                                                Sorry, nothing to display here :(
                                            </template>
                                        </v-data-table>
                                    </v-card>
                                </template>

                                <app-dialog-tag
                                        v-bind:dialog="dialog"
                                        v-bind:item="editedItem"
                                        v-on:close="dialog = $event"
                                        v-on:clear="editedItem = $event"
                                ></app-dialog-tag>

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
    import debounce from 'debounce'
    import DialogTag from '../../components/Blog/dialogTag'

    export default {
        name: "Tag",
        components: {
            appDialogTag: DialogTag,
        },
        data() {
            return {
                pagination: {
                    sortBy: 'name',
                    rowsPerPage: 25 // -1 for All",
                },
                search: '',
                filteredData: [],
                headers: [
                    {text: 'title', align: 'center', sortable: true, value: 'title'},
                    {text: 'status', align: 'center', sortable: true, value: 'status'},
                    {text: 'created', align: 'center', sortable: true, value: 'created'},
                    {text: 'action', align: 'center', sortable: false},
                ],
                dialog: false,
                editedItem: {},
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
                this.$store.dispatch('loadPostList', {})
                    .then(() => {
                        this.filteredData = this.Post
                    })
            },
            searchData() {
                if (this.search == '') {
                    this.filteredData = this.Post
                } else {
                    this.filteredData = []
                    for (let i = 0; i < this.Post.length; i++) {
                        let s = ''
                        for (let key in this.Post[i]) {
                            if (this.Post[i][key] != null)
                                if (typeof (this.Post[i][key]) != 'boolean')
                                    s += this.Post[i][key].toString().toLowerCase()
                        }
                        if (s.includes(this.search.toLocaleLowerCase()))
                            this.filteredData.push(this.Post[i])
                    }
                }
            },
            editItem(item) {
                this.editedItem = Object.assign({}, item)
                this.dialog = true
            },
            deleteItem(item) {
                item.deleted = !item.deleted
                this.$store.dispatch('savePost', item)
            },
            addNem() {
                this.dialog = true
            },
            postStatus(value) {
                if (value == 0)
                    return 'DRAFT'
                else if (value == 1)
                    return 'HIDDEN'
                else if (value == 2)
                    return 'PUBLISHED'
                else
                    return 'UNKNOWN'
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
            Post() {
                return this.$store.getters.Post
            },


        },
        watch: {}
    }
</script>

<style scoped>

</style>