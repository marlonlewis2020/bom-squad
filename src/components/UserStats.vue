<template>
    <div class="container-fluid stats">
        <div class="card">
            <div class="card-body">
                <div class="image">
                    <img class="" :src="`../../uploads/${user.image_url}`" alt="user avatar">
                </div>
                <div class="details">
                    <h5 class="h5 card-title">{{ user.firstname }} {{ user.lastname }}</h5>
                    <p>
                        <small>
                            {{ user.location }}
                        </small>
                    </p>
                    <p>
                        <small>
                            Member since {{ user.date }}
                        </small>
                    </p>
                    <p>
                        <small>
                            {{ user.biography }}
                        </small>
                    </p>
                </div>
                <div class="follow">
                    <div class="following">
                        <div id="posts" class="socials float-left">
                            <span class="small">{{ user.posts }}</span>
                            <span class="h6">Posts</span>
                        </div>
                        <div id="followers" class="socials float-right">
                            <span class="small">{{ user.followers }}</span>
                            <span class="h6">Followers</span>
                        </div>
                    </div>
                    <button v-if="!user.me && !user.followed" id="follow-btn" class="btn btn-primary" @click="follow()">Follow</button>
                    <button v-if="!user.me && user.followed" id="follow-btn" class="btn btn-primary" @click="unfollow">Un-Follow</button>
                </div>
            </div>
        </div>

    </div>
</template>
<script setup lang="ts">

    let prop = defineProps(['user']);
    let emit = defineEmits(['follow', 'unfollow']);
    

    function follow() {
        emit('follow');
    }

    function unfollow() {
        emit('unfollow');
    }
</script>

<style scoped>
    .card-body, .following {
        display: flex;
        flex-direction:row;
    }
    
    .image {
        max-width:256px;
        padding: 0 15px 0 0;
        width:100%;
        /* margin:auto; */
    }

    .image img {
        width:100%;
        height:100%;
    }
    
    .card {
        width:100%;
        height: fit-content;
        box-shadow: 2px 2px 2px gray;
    }

    @media (min-width:990px) {
        
        .details {
            position:relative;
            width:100%;
        }

        .follow, .details {
            display:flex;
            flex-direction: column;
        }

        .follow {
            right:15px;
            width:100%;
        }

        .h6, h6 {
            font-size:1rem;
        }

        
    }

    @media (min-width:820px) and (max-width: 990px) {
        .container {
            height:fit-content;
        }
        .details {
            position:relative;
            left:15px;
            width:45%;
        }

        .follow, .details {
            display:flex;
            flex-direction: column;
        }

        .follow {
            position:absolute;
            top:380px;
            right:15px;
            width:45%;
        }
        .card {
            width:100%;
            height:fit-content;
        }

        .card-body {
            width:100%;
            display:flex;
            flex-direction: column;
        }

        .h6, h6 {
            font-size:1rem;
        }

        .image {
            width:100%;
            height:30vh;
            padding:auto;
            margin:auto;
        }

        .image img {
            width:100%;
            height:25vh;
            padding:0;
            margin:0;
        }

    }

    @media (min-width:412px) and (max-width: 820px) and (max-height:720px) {

        .container {
            height:fit-content;
        }
        .details {
            position:relative;
            left:15px;
            width:45%;
        }

        .follow, .details {
            display:flex;
            flex-direction: column;
        }

        .follow {
            position:absolute;
            top:180px;
            right:15px;
            width:45%;
        }
        .card {
            width:100%;
            height:fit-content;
        }

        .card-body {
            width:100%;
            display:flex;
            flex-direction: column;
        }

        .h6, h6 {
            font-size:1rem;
        }

        .image {
            width:100%;
            height:30vh;
            padding:auto;
            margin:auto;
        }

        .image img {
            width:100%;
            height:25vh;
            padding:0;
            margin:0;
        }
    }

    @media (min-width:412px) and (max-width: 820px) and (min-height:725px) {

        .container {
            height:fit-content;
        }
        .details {
            position:relative;
            left:15px;
            width:45%;
        }

        .follow, .details {
            display:flex;
            flex-direction: column;
        }

        .follow {
            position:absolute;
            top:288px;
            right:15px;
            width:45%;
        }
        .card {
            width:100%;
            height:fit-content;
        }

        .card-body {
            width:100%;
            display:flex;
            flex-direction: column;
        }

        .h6, h6 {
            font-size:1rem;
        }

        .image {
            width:100%;
            height:30vh;
            padding:auto;
            margin:auto;
        }

        .image img {
            width:100%;
            height:25vh;
            padding:0;
            margin:0;
        }

    }

    @media (max-width:412px) {
        
        .card {
            width:100%;
        }

        .card-body {
            width:100%;
            display:flex;
            flex-direction: column;
        }

        .h6, h6 {
            font-size:1rem;
        }

        .image {
            width:100%;
            height:30vh;
            padding:auto;
            margin:auto;
        }

        .image img {
            width:100%;
            height:100%;
            padding:0;
            margin:0;
        }

    }

    .details {
        margin-top: 25px;
    }


    .following {
        margin-top:45px;
        text-align: center;
    }

    .socials {
        width: 45%;
        display:flex;
        flex-direction: column;
        padding: 1px 1px;
    }

    #follow-btn {
        margin-top: 50px;
        width: 100%;
    }
</style>