<template>
    <h3 class="h3">Login</h3>
    <div class="container form-container">
        <form class="col-sm-12" id="loginForm" action="" method="post" @submit.prevent="login">
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input v-model="login_un" type="text" id="username" name="username" class="form-control" maxlength="80" />
            </div>
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="login_pw" type="password" id="password" name="password" class="form-control" />
            </div>
            <button type="submit" name="submit" id="submit" class="btn btn-success d-flex text-center"> Submit </button>
        </form>
    </div>
</template>

<script setup lang="ts">
    
    import { ref } from "vue";

    const emits = defineEmits<{
        (event: 'fail', errors:any, message:string): void
        (event: 'success'): void
    }>();

    let status = ref("");
    let errors = ref([]);
    let message = ref("");
    let login_un = ref("");
    let login_pw = ref("");

    function fail():void {
        emits('fail', errors.value, message.value);
    }

    function success():void {
        emits('success');
    }

    function clearLogin() {
        login_un.value = "";
        login_pw.value = "";
    }

    function clear() {
        errors.value = [];
        message.value = "";
        clearLogin();
        setTimeout(()=>{
            status.value = "";
        },4*1000);
    }

    function login() {
        if (!localStorage['id']) {
            const data = new FormData($('form#loginForm')[0]);
            const url = "/api/v1/auth/login";
    
            fetch(url, {
                method: 'POST',
                headers: {
                    // 'Accept': 'application/json'
                },
                body: data
            })
            .then(function (response: any): any {
                const res = response.json();
                return res;
            })
            .then((data) => {
                if (data.status!=="success") {
                    // recover from fail with some operation or message
                    status.value = "error";
                    errors.value = data.errors;
                    message.value = data.message;
                    console.log("login failed");
                    fail();
                } else {
                    status.value = "success";
                    clearLogin();
                    // persistent storage of authorization token
                    localStorage["token"] = data.token ;
                    let id = localStorage["id"] = data.id ;
                    success();
                    clear();
                    console.log("login successful");
                    emits('success');
                }
            });
        }

    }
    

</script>

<style scoped>
    #submit {
        width:100%;
        margin-top:50px;
        /* margin: 0 auto; */
    }

    .form-container {
        padding:50px;
        background-color:white;
        border-radius: 5px;
        box-shadow: 1px 1px 5px gray;
    }

    .h3 {
        margin-bottom: 20px;
    }

    button {
        justify-content: center;
    }
</style>