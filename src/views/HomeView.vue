<script setup lang="ts">
  import TheHome from '../components/TheHome.vue'
  import UserProfile from '../components/UserProfile.vue'
  let id = localStorage['id'];
  if(id) {
    window.location.replace('/dashboard');
  } 
  
</script>

<template>
  <main>
    <Suspense>
      <TheHome #default v-if="!id" :id="id" />
      <template #fallback>Loading...</template>
    </Suspense>
  </main>
</template>
