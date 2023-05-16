<template>
    <div class="stats">
        <UserStats @follow="follow" @unfollow="unfollow" v-bind:user="user" />
    </div>
    <div class="photos">
        <UserPhotos class="pic" v-for="photo, index in photos" v-bind:photo="photo" v-bind:key="index" @click="view(index)" data-toggle="modal" data-target="#viewpostmodal" />
    </div>

    <div id="viewpostmodal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="preview" aria-hidden="true">
        <div class="modal-dialog .modal-dialog-centered">
            <div class="modal-content card">
                <div class="modal-body ">
                    <img class="preview card-image" :src="`../../uploads/${post['photo']}`" alt="image"/>
                </div>
                <div class="label" id="label" hidden>preview image</div>
            </div>
        </div>
    </div>

</template>
<script setup lang="ts">
    import { ref, onMounted, onBeforeMount } from 'vue'
    import UserStats from '../components/UserStats.vue'
    import UserPhotos from '../components/UserPhotos.vue'
    let emit = defineEmits(['logout']);

    let photos = ref([]);
    let user = ref({});
    let id:string = localStorage['id'];
    let userid:Number = Number(location.pathname.split("/")[2]);
    let me:boolean = userid == Number(id);
    var post = ref({});
    let posts:any = [];

    
    onBeforeMount(() => {
        let user_url:string = `/api/v1/users/${userid}`;

        fetch(user_url,{
            method:'GET',
            headers:{
                'Authorization':`bearer ${localStorage['token']}`
            }
        })
        .then((result)=>{
            return result.json();
        })
        .then((json_obj)=>{
            if (json_obj.status == "success") {
                let data = json_obj.user;
                let image_url = data.image_url;
                let firstname = data.firstname;
                let lastname = data.lastname;
                let location = data.location;
                let date = data.date;
                let postsdata = data.posts;
                let followers = data.followers;
                let biography = data.biography;
                let followed = data.followed;
                photos.value = json_obj.photos;
                user.value = {
                    image_url: image_url,
                    firstname: firstname[0].toUpperCase() + firstname.substring(1).toLowerCase(),
                    lastname: lastname[0].toUpperCase() + lastname.substring(1).toLowerCase(),
                    location: location.toUpperCase(),
                    date: date,
                    posts: postsdata,
                    followers: followers,
                    biography: biography,
                    userid:userid,
                    followed:followed,
                    me:me
                }
                posts = json_obj.posts;
            } else {
                if (json_obj.type) {
                    emit('logout');
                }
            }
        });
    });

    function view(index: string|number):void {
        post.value = posts[Number(index)];
        console.log(index);
    }

    function follow() {
        if (!me){
            fetch(`/api/v1/follow/${userid}`, {
                method:"POST",
                headers: {
                    "Authorization": `bearer ${localStorage['token']}`
                }
            })
            .then(result => result.json())
            .then((data) => {
                if (data.status == "success") {
                    user.value['followed']=true;
                    user.value['followers']+=1;
                }
            })

        }
    }

    function unfollow() {
        if (!me){
            fetch(`/api/v1/unfollow/${userid}`, {
                method:"POST",
                headers: {
                    "Authorization": `bearer ${localStorage['token']}`
                }
            })
            .then(result => result.json())
            .then((data) => {
                if (data.status == "success") {
                    user.value['followed']=false;
                    user.value['followers']-=1;
                }
            })

        }
    }

</script>

<style scoped>

    .photos {
        margin-top:35px;
        height:300px;
    }

    @media (min-width:410px) and (max-width:550px) {
        .photos {
            width:100%;
            display:grid;
            grid-template-columns: 1fr 1fr;
        }
    }

    @media (min-width:550px) {
        .photos {
            width:100%;
            height:300px;
            display:grid;
            grid-template-columns: 1fr 1fr 1fr;
        }
    }

    .container {
        width:100%;
        height:fit-content;
        display:flex;
        flex-direction:column;
        margin-left:0;
    }

    #viewpostmodal {
        justify-content: center;
        align-items:center;
        vertical-align: middle;
    }

    .modal-body {
        height:100%;
        padding:0;
        margin:0;
    }

    #viewpostmodal .preview {
        width:100%;
    }

    .stats {
        width:100vw;
    }

    .pic {
        width:100%;
        height:300px;
    }

</style>