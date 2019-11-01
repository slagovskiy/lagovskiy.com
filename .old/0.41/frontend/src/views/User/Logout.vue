<template>
    <div></div>
</template>

<script>
    export default {
        name: 'app',
        created() {
            this.$store
                .dispatch('logout')
                .then(() => {
                    this.$router.push('/')
                })
                .catch(() => {})
            }
    }
</script>

<style scoped>

</style>
