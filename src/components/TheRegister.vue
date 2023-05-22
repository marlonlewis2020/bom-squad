<template>
    <div class="form">
        <div class="modal-content">
            <div class="modal-header">
                <h5>New Customer</h5>
                <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" >x</button>
            </div>

            <div class="modal-body">
                
                <form id="register" enctype="multipart/form-data" method="POST">
                    <div class="form-group address">
                        
                        <h1>Address</h1>
                        <div class="form-group">
                            <label for="address_line_1">Address Line 1</label>
                            <input id="address_line_1" name="address_line_1" type="text" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="city"> City</label>
                            <input id="city" name="city" type="text" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="parish"> Parish</label>
                            <select id="parish" name="parish" type="text" class="form-control" required>
                                <option value=""></option>
                                <option value="Clarendon">Clarendon</option>
                                <option value="Hanover">Hanover</option>
                                <option value="Kingston">Kingston</option>
                                <option value="Manchester">Manchester</option>
                                <option value="Portland">Portland</option>
                                <option value="St. Andrew">St. Andrew</option>
                                <option value="St. Ann">St. Ann</option>
                                <option value="St. Catherine">St. Catherine</option>
                                <option value="St. Elizabeth">St. Elizabeth</option>
                                <option value="St. James">St. James</option>
                                <option value="St. Mary">St. Mary</option>
                                <option value="St. Thomas">St. Thomas</option>
                                <option value="Trelawny">Trelawny</option>
                                <option value="Westmoreland">Westmoreland</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="country"> Country</label>
                            <select id="country" name="country" type="text" class="form-control" required>
                                <option value="Jamaica">Jamaica</option>
                                <option value="other">other</option>
                            </select>
                        </div>
                        <div class="form-group" hidden>
                            <label for="postal_code"> Postal Code</label>
                            <input id="postal_code" name="postal_code" type="text" class="form-control" value="JMAKN04" hidden>
                        </div>
                    </div>

                    <div class="form-group company details">
                        <h1>Company Details</h1>
                        <div class="form-group">
                            <label for="company">Company</label>
                            <input id="company" name="company" type="text" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="branch">Branch</label>
                            <input id="branch" name="branch" type="text" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="officer">Purchasing Officer</label>
                            <input id="officer" name="officer" type="text" class="form-control">
                        </div>
                    </div>

                    <div class="form-group">
                        <h1>Personal Details</h1>
                        <div class="form-group">
                            <label for="name">Full Name</label>
                            <input id="name" name="name" type="text" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="contact_number">Contact Number</label>
                            <input id="contact_number" name="contact_number" type="text" class="form-control" maxlength="10">
                        </div>
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input id="email" name="email" type="email" class="form-control">
                        </div>
                    </div>

                    <div class="form-group">
                        <h1>Login Details</h1>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input id="username" name="username" type="text" class="form-control" rows="2" cols="20" wrap="hard" maxlength="80">
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input id="password" name="password" type="password" class="form-control">
                            <!-- <label for="confirm">Confirm</label> -->
                            <!-- <input v-model="conf_pwd" id="confirm" name="confirm" type="password" class="form-control"> -->
                        </div>
                    </div>
                    <input type="hidden" name="role" value="customer">
                    <button @click="register" class="btn btn-primary" value="save">Register</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup >

    import {ref} from 'vue'

    function register(event) {
        event.preventDefault();

        let form = new FormData($('form#register')[0])
        let url = "/api/v1/customers";

        fetch(url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json'
            },
            body: form
        })
        .then(result => result.json())
        .then((data) => {
            if (data.status==="success") {
                console.log('user registered');
                window.location.assign('/dashboard');
                
            } else {
                console.log('Registration Failed! Contact System Administrator.');
                alert("Registration Failed! Contact System Administrator.")
                $('form#register').trigger('reset');
            }
        })
    

        
    }
</script>

<style scoped>

    .modal-header {
        background-color:rgb(89, 89, 152);
        color:aliceblue;
    }

    .btn-close {
        border-width: 0;
        border-color: rgb(182, 98, 98);
        border-radius: 5px;
        background-color: rgb(182, 98, 98);
        color: rgb(64, 64, 64);
        font-weight: 600;
        font-family: monospace;
        margin-top:2px;
        margin-right:2px
    }

    .btn {
        margin-top: 25px;
        width:100%;
    }

    h5 {
        margin-bottom: 20px;
    }

    .form {
        background-color: white;
        /* box-shadow:5px 5px 10px gray; */
        margin-bottom: 30px;
        border-radius: 5px;
    }

    .form-group {
        margin-top: 15px;
    }

    #register {
        padding:15px;
    }
</style>