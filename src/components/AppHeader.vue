<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <div class="brand">
          <a v-if="login" class="navbar-brand" :href="`/users/${id}`"><img class="camera-img" src="./icons/oil-tanker.png" alt="camera image"> Truck Scheduling</a>
          <a v-else class="navbar-brand" href="/"><img class="camera-img" src="./icons/oil-tanker.png" alt="camera image"> Truck Scheduling</a>
        </div>
        <div class="menu float-end">
          <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="nav navbar-nav me-auto">
              <li v-if="!login">
                <RouterLink v-bind:id='id' class="text-white" to="/">Home</RouterLink>
              </li>
              <li v-if="login">
                <RouterLink class="text-white" to="/dashboard">Dashboard</RouterLink>
              </li>
              <li v-if="login" >
                <a class="text-white" @click="logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
  import { RouterLink } from "vue-router";
  let login:boolean = localStorage['token']? true : false;
  let id: number = localStorage['id'] ?? 0;

  function logout() {
    const url: string = "/api/v1/auth/logout"; 
    fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `bearer ${localStorage['token']}`
        }
    })
    .then((data)=>{
        // update the token and id in localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('id');
        window.location.assign("/");
    });
  }
</script>

<style scoped>
  /* Add any component specific styles here */
  @import url('https://fonts.googleapis.com/css2?family=Lobster');

  .navbar {
    margin-bottom: 30px;
  }
  .navbar-brand {
    font-family: 'Lobster', sans-serif;
  }

  .camera-img {
    width:24px;
    padding-bottom: 10px;
    padding-right: 6px;
  }
  header {
    margin-bottom: 200px;
  }

  a {
    text-decoration-line: none;
    -moz-text-decoration-line: none;
  }

  ul.nav li a, ul.nav li a:visited {
    color: white !important;
  }

  li {
    width:80px;
    margin: 0 10px;
  }

  a:hover {
    font-weight: bold;
  }
</style>