<template>
    <main>
        <dev class="container">
            <UserProfile @logout="logout" />
        </dev>
    </main>
</template>

<script setup lang="ts">
    import UserProfile from '../components/UserProfile.vue'

    function logout() {
        localStorage.removeItem('id');
        localStorage.removeItem('token');
        window.location.assign('/login');
    }
</script>