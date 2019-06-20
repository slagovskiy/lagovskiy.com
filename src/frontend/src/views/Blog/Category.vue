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
                                    <v-data-table
                                            v-bind:items="Category"
                                            class="elevation-1"
                                    >
                                         <template v-slot:items="props">
                                            <td>{{ props.item.name }}</td>
                                            <td class="text-xs-right">{{ props.item.slug }}</td>
                                            <td class="text-xs-right">{{ props.item.title }}</td>
                                            <td class="text-xs-right">{{ props.item.deleted }}</td>
                                        </template>
                                    </v-data-table>
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
            return {}
        },
        mounted() {
            this.$store.dispatch('loadCategoryList', {})
        },
        methods: {},
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
            }
        }
    }
</script>

<style scoped>

</style>