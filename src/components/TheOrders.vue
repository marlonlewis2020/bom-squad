<template>
    <!-- <div id="component" class="container">
        <div class="card">
            <div class="card-header">
                <div class="profile_pic flex-start">
                    <img class="" :src="`../../uploads/${post.profile_photo}`" alt="profile_pic">
                    
                    <a :href="`/users/${post.user_id}`">{{ post.username }}</a>
                </div>
            </div>
            <div class="card-image">
                <img class="" :src="`../../uploads/${post.photo}`" alt="post image">
            </div>
            <div class="card-body">
                <p class="card-text">
                    {{ post.caption }}
                </p>
            </div>
            <div class="container footer">
                <span class="likes float-left">
                    <img v-if="post.liked" class="full" src="../components/icons/full_heart.png" alt="like post" @click="unlike(post.id)" />
                    <img v-else class="empty" src="../components/icons/empty_heart.png" alt="unliked post" @click="like(post.id)" />
                    <small>{{ post.likes }} likes</small>
                </span>
                <span class="date float-right">
                    <small>{{ post.created_on }}</small>
                </span>
            </div>
        </div>
    </div> -->

</template>

<script setup lang="ts">

    // let props = defineProps(['post']);
    // let emit = defineEmits<{
    //     (event: 'like', index: number): void
    //     (event: 'unlike', index: number): void
    // }>();

    // function like(index:number) {
    //     emit('like',index);
    // }

    // function unlike(index:number) {
    //     emit('unlike', index);
    // }

</script>

<style scoped>

    #component {
        min-width: 100%;
    }

    .card {
        max-width:400px;
        height:450px;
        
        margin-bottom:25px;
    }

    .card-header {
        height:fit-content;
        background-color: white;
        border:none;
    }

    .profile_pic img {
        width:28px;
        margin-right:8px;
        border-radius:50%;
    }

    .likes img {
        position:absolute;
        width:24px;
        padding-right:10px;
    }

    .likes .empty:hover {
        width:26px;
        /* padding-right:8px; */
    }
    
    .likes small {
        position:absolute;
        left:35px;
    }

    .date:hover, .likes:hover {
        color:gray;
    }
    
    .card-image, .card-image img {
        width:100%;
        height:250px;
    }

    .card-body {
        height: 100%;
    }

    .card-text {
        height: 100%;
        margin-bottom:50px;
    }

    .footer {
        padding-bottom:10px;
        cursor:default;
    }

    .footer small {
        margin-left: 15px;
    }

    .footer, .profile_pic {
        font-size: smaller;
        color:rgb(102, 102, 102);
        font-weight:700;
        font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
    }

</style>