<template>
    <div class="photo">
        <img class="container-fluid" :src="`../../uploads/${photo}`" :alt="photo" @click="view">
    </div>
</template>
<script setup lang="ts">

    let prop = defineProps(['photo']);
    let emit = defineEmits(['click']);

    function view() {
        emit('click');
    }
    
</script>
<style scoped>
    img, .photo {
        width:100%;
        height:300px;
        margin: auto 2px;
        padding-bottom:15px;
    }

</style>