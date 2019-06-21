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
                                            <v-spacer></v-spacer>
                                            <v-text-field
                                                    v-model="search"
                                                    append-icon="fa-search"
                                                    label="Search"
                                                    single-line
                                                    hide-details
                                            ></v-text-field>
                                        </v-card-title>
                                        <v-data-table
                                                v-bind:items="filteredItems"
                                                v-bind:headers="headers"
                                                v-bind:pagination.sync="pagination"
                                                v-bind:loading="loading"
                                                prev-icon="fa-caret-left"
                                                next-icon="fa-caret-right"
                                                sort-icon="fa-arrow-up"
                                                class="elevation-1"
                                        >
                                            <template v-slot:items="props">
                                                <td class="text-xs-left">{{ props.item.name }}</td>
                                                <td class="text-xs-left">{{ props.item.slug }}</td>
                                                <td class="text-xs-center">{{ props.item.order }}</td>
                                                <td class="text-xs-center">{{ props.item.deleted }}</td>
                                            </template>
                                            <template v-slot:no-data>
                                                Sorry, nothing to display here :(
                                            </template>
                                        </v-data-table>
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
                >
                    Access denied!
                </v-alert>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        name: "Category",
        data() {
            return {
                pagination: {
                    sortBy: 'name',
                    rowsPerPage: 25 // -1 for All",
                },
                search: '',
                headers: [
                    {text: 'name', align: 'center', sortable: true, value: 'name'},
                    {text: 'slug', align: 'center', sortable: true, value: 'slug'},
                    {text: 'order', align: 'center', sortable: true, value: 'order'},
                    {text: 'deleted', align: 'center', sortable: true, value: 'deleted'},
                ]
            }
        },
        mounted() {
            this.$store.dispatch('loadCategoryList', {})
        },
        methods: {
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
            filteredItems: function () {
                return this.Category.filter(function (item, s=this.search) {
                    var tmp = JSON.stringify(item)
                    return tmp.includes(s)

                })
            }
        }
    }
</script>

<style scoped>

</style>