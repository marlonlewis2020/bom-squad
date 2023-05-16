<template>
    <div class="container col-sm-8 col-lg-5">
        <div v-if="displayAlerts" :class="[(status=='success' || status=='error')? (( status!=='success' ) ? alertDanger : alertSuccess) : 'alert']">
            <ul v-if="status=='error'">
                <li v-for="(error, indx) in errors" v-bind:errors="errors" v-bind:key="indx">
                    {{ error }}
                </li>
            </ul>
            <span v-else>{{ message }}</span>
        </div>
        <LoginForm @success='success' @fail="fail"/>
    </div>
</template>

<script setup lang="ts">
    import LoginForm from './LoginForm.vue';
    import { ref } from 'vue';

    // let id:string = localStorage['id'] ;

    if (localStorage['id']) {
        success();
    } 

    let displayAlerts = ref(false);
    let status = ref("");
    let errors = ref([""]);
    let message = ref("");
    const alertDanger: string = "alert alert-success";
    const alertSuccess: string = "alert alert-dander";

    function fail(e: string[], m: string) {
        status.value = "error";
        errors.value = e;
        message.value = m;
        alert("Login Failed. Try again.");
        // location.reload();
    }

    function success() {
        location.assign("/dashboard");
    }
</script>

