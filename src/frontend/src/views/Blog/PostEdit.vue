<template>
    <v-container grid-list-md fluid class="pt-0 pb-0 pl-0 pr-0">
        <v-layout row wrap v-if="isAuthenticated">
            <v-flex xs12>
                <v-card>
                    <v-card-title>
                        <span class="headline">{{ formTitle}}</span>
                    </v-card-title>
                    <v-card-text>
                        <v-tabs fixed-tabs v-bind:model="activeTab">
                            <v-tab v-bind:key="1">Main</v-tab>
                            <v-tab v-bind:key="2">CEO</v-tab>
                            <v-tab v-bind:key="3">Comment</v-tab>
                            <v-tab v-bind:key="4">Edit</v-tab>

                            <v-tab-item v-bind:key="1">
                                <v-text-field
                                        label="title"
                                        v-model="editedItem.title"
                                ></v-text-field>
                                <v-text-field
                                        label="slug"
                                        v-model="editedItem.slug"
                                ></v-text-field>
                                <v-checkbox
                                        v-model="editedItem.sticked"
                                        label="sticked"
                                ></v-checkbox>
                                <v-select
                                        v-bind:items="postStatus"
                                        v-model="editedItem.status"
                                        item-text="text"
                                        item-value="id"
                                        label="status"
                                ></v-select>
                                <v-text-field
                                        label="published"
                                        v-model="editedItem.published"
                                ></v-text-field>
                            </v-tab-item>
                            <v-tab-item v-bind:key="2">
                                <v-textarea
                                        label="description"
                                        v-model="editedItem.description"
                                ></v-textarea>
                                <v-textarea
                                        label="keywords"
                                        v-model="editedItem.keywords"
                                ></v-textarea>
                                <v-input>
                                    <v-select
                                            v-bind:items="Category"
                                            v-model="editedItem.categories"
                                            item-text="name"
                                            item-value="id"
                                            label="category"
                                            chips
                                            multiple
                                    ></v-select>
                                    <v-btn color="primary" dark v-on:click="editedItemCategory = {}; dialogCategory = true">Add category</v-btn>
                                    <app-dialog-category
                                            v-bind:dialog="dialogCategory"
                                            v-bind:item="editedItemCategory"
                                            v-on:close="dialogCategory = $event"
                                            v-on:clear="addNewCategory($event)"
                                    ></app-dialog-category>
                                </v-input>
                                <v-input>
                                    <v-select
                                            v-bind:items="Tag"
                                            v-model="editedItem.tags"
                                            item-text="name"
                                            item-value="id"
                                            label="tag"
                                            chips
                                            multiple
                                    ></v-select>
                                    <v-btn color="primary" dark v-on:click="editedItemTag = {}; dialogTag = true">Add tag</v-btn>
                                    <app-dialog-tag
                                            v-bind:dialog="dialogTag"
                                            v-bind:item="editedItemTag"
                                            v-on:close="dialogTag = $event"
                                            v-on:clear="addNewTag($event)"
                                    ></app-dialog-tag>
                                </v-input>
                                <v-checkbox
                                        v-model="editedItem.do_ping"
                                        label="do ping"
                                ></v-checkbox>
                                social image
                            </v-tab-item>
                            <v-tab-item v-bind:key="3">
                                <v-checkbox
                                        v-model="editedItem.comments_enabled"
                                        label="comments enabled"
                                ></v-checkbox>
                                <v-checkbox
                                        v-model="editedItem.comments_moderated"
                                        label="comments moderated"
                                ></v-checkbox>
                            </v-tab-item>
                            <v-tab-item v-bind:key="4">
                                <v-textarea
                                        v-model="editedItem.teaser"
                                        label="teaser"
                                ></v-textarea>
                                <v-textarea
                                        v-model="editedItem.content"
                                        label="content"
                                ></v-textarea>
                            </v-tab-item>
                        </v-tabs>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="" v-on:click="goBack">Cancel</v-btn>
                        <v-btn color="primary">Save</v-btn>
                    </v-card-actions>
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
    import DialogCategory from '../../components/Blog/dialogCategory'
    import DialogTag from '../../components/Blog/dialogTag'

    export default {
        name: "PostEdit",
        components: {
            appDialogCategory: DialogCategory,
            appDialogTag: DialogTag
        },
        data() {
            return {
                defaultItem: {
                    id: -1,
                    slug: '',
                    title: '',
                    description: '',
                    keywords: '',
                    status: 0,
                    sticked: false,
                    comments_enabled: true,
                    comments_moderated: true,
                    do_ping: false,
                    published: '',
                    categories: [],
                    tags: [],
                    teaser: '',
                    content: '',
                    social_image: null
                },
                dialogCategory: false,
                editedItemCategory: {},
                dialogTag: false,
                editedItemTag: {},
                activeTab: null,
                formTitle: 'Post edit',
                editedItem: {},
                postStatus: [
                    {id: 0, text: 'DRAFT'},
                    {id: 1, text: 'HIDDEN'},
                    {id: 2, text: 'PUBLISHED'},
                ],
                menuPublishedDate: false
            }
        },
        props: {
            id: Number
        },
        mounted() {
            this.$store.dispatch('loadCategoryList')
            this.$store.dispatch('loadTagList')
            if (this.id === -1) {
                this.editedItem = Object.assign({}, this.defaultItem)
            } else {
                for (let i = 0; i < this.Post.length; i++)
                    if (this.Post[i].id == this.id) {
                        this.editedItem = Object.assign({}, this.Post[i])
                        break
                    }
            }
        },
        methods: {
            goBack() {
                this.$router.push({name: 'blog-post'})
            },
            addNewCategory(item) {
                this.editedItem.categories.push(item.id)
            },
            addNewTag(item) {
                this.editedItem.tags.push(item.id)
            },
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
            Category() {
                return this.$store.getters.Category
            },
            Tag() {
                return this.$store.getters.Tag
            }
        }
    }
</script>

<style scoped>

</style>