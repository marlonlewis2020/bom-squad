<template>
    
    <div v-if="deliveries.length" class="row-fluid schedule">
        <TodaySchedule :deliveries="prop.deliveries"/>
    </div>
</template>

<script setup lang="ts">
    import TodaySchedule from '../components/TodaySchedule.vue';

    const prop = defineProps(['deliveries']);

</script>

<style scoped>
    .schedule {
        width:100%;
        margin-top:15px;
    }
</style>