<template>
    <div></div>
</template>

<script>
    export default {
        name: "Home",
        data() {
            return {}
        },
        methods: {},
        computed: {
            isAuthenticated() {
                return this.$store.getters.isAuthenticated
            },
        }
    }
</script>

<style scoped>

</style>