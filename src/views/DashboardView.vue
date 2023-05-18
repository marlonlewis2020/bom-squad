<script setup >
  import { ref, onMounted } from 'vue'
  import TheOrders from '../components/TheOrders.vue'
  
  let id  = Number(localStorage['id']);
  let url = `/api/v1/customers/${id}`;
  let customer;
  let order = `/api/v1/orders`;

  let delivery_date = ref("");
  let delivery_time = ref("");
  let quantity = 0;
  let q_diesel = ref(0);
  let q_87 = ref(0);
  let q_90 = ref(110);
  let q_ulsd = ref(0);
  let preferred = ref("90");
  let location;
  let customer_id;
  
  onMounted(() => {
    fetch(url, {
        method: 'GET',
        headers: {
            // token: `bearer ${localStorage['token']}`
      }
    })
    .then((result)=>{
        return result.json();
    })
    .then((data) => {
        if (data.status == "success") {
          customer = data.data;
          location = customer['address_id'];
          customer_id = customer['customer_id'];
        } else {
          console.log(data.message);

        }
    });

  });


  function addOrder() {
    if (id && typeof id == 'number') {
      console.log("Create Order function called");

      fetch("/api/v1/orders", {
          method: 'POST',
          headers: {},
          body: new FormData($('form#createOrderForm')[0])
      })
      .then((result)=>{
          return result.json();
      })
      .then((data)=>{
          if (data.status == "success") {
            console.log("order created successfully");
            location.reload();
          } else {
              console.log("failed to create order");
          }
      });
    }
  }

  function updateQuantity() {
    quantity = Number(q_diesel.value) + Number(q_87.value) + Number(q_90.value) + Number(q_ulsd.value);
   }

</script>

<template>
  <main>
    <div class="container">
      
      <button 
        v-if="id" 
        @click="clear"
        type="button" 
        value="New Order" 
        class="new_post text-center btn btn-primary float-end" 
        data-toggle="modal" 
        data-target="#addordermodal">
        New Order
      </button>
        <TheOrders #default class="float-start" v-for="cus in customer" />   
        <div id="addordermodal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalLabel"> Place Order</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" >x</button>
                </div>
                <div class="modal-body">
                    <form id="createOrderForm" action="" method="post" enctype="multipart/form-data">
                        <div class="form-group">
                          <input :value="customer_id" name="customer_id" id="customer_id" cols="30" rows="2" class="form-control" maxlength="75" hidden>
                          <div class="form-group">
                            <label for="caption">Delivery Date</label>
                            <input v-model="delivery_date" type="date" name="delivery_date" id="delivery_date" cols="30" rows="2" class="form-control" maxlength="75" >
                          </div>
                          <div class="form-group">
                            <label for="caption">Delivery Time</label>
                            <select v-model="delivery_time" name="delivery_time" id="delivery_time" cols="30" rows="2" class="form-control" maxlength="75">
                              <option value="8:00 AM">8:00 AM</option>
                              <option value="12:00 PM">12:00 PM</option>
                              <option value="4:00 PM">4:00 PM</option>
                            </select>
                          </div>
                          <div class="form-group" hidden>
                            <label for="caption">Quantity</label>
                            <input v-model="quantity" name="quantity" id="quantity" cols="30" rows="2" class="form-control" maxlength="75" v-on:change="updateQuantity">
                          </div>
                          <div class="form-group">
                            <label for="caption">Diesel</label>
                            <input v-model="q_diesel" type="number" name="q_diesel" id="q_diesel" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group">
                            <label for="caption">87</label>
                            <input v-model="q_87" type="number" name="q_87" id="q_87" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group">
                            <label for="caption">90</label>
                            <input v-model="q_90" type="number" name="q_90" id="q_90" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group">
                            <label for="caption">ulsd</label>
                            <input v-model="q_ulsd" type="number" name="q_ulsd" id="q_ulsd" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group" hidden>
                            <label for="caption">Price</label>
                            <input value="0.00" type="decimal" name="price" id="price" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group" hidden>
                            <label for="caption">Status</label>
                            <input value="Pending" name="status" id="status" cols="30" rows="2" class="form-control" maxlength="75" hidden>
                          </div>
                          <div class="form-group" hidden>
                            <label for="caption" >Address</label>
                            <input :value="location" type="text" name="location" id="location" cols="30" rows="2" class="form-control" maxlength="75">
                          </div>
                          <div class="form-group">
                            <label for="caption">Preference</label>
                            <select v-model="preferred" name="preferred" id="preferred" cols="30" rows="2" class="form-control" maxlength="75">
                              <option value="diesel">diesel</option>
                              <option value="87">87</option>
                              <option value="90">90</option>
                              <option value="ulsd">ulsd</option>
                            </select>
                          </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" 
                      v-on:click="addOrder" 
                      class="btn btn-primary">
                        <img id="save" src="../components/icons/save.png" alt="save" class="text-white" />  
                        Save
                    </button>
                    <button 
                      type="button" 
                      class="btn btn-secondary"
                      @click="clear" 
                      data-dismiss="modal">
                        Close
                    </button>
                </div>
            </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

  .preview {
    width: 100%;
    justify-content: center;
    margin:auto auto 15px auto;
  }

  #preview-image {
    width:100%;
    height:400px;
  }

  input[type="file"] {
    width: 110px;
    border: none;
    background-color: none;
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

  .btn-close:hover {
    font-weight:800;
    border-color: brown;
    background-color: red;
    color:white;
    box-shadow: 1px 1px 3px black;
  }

  #save {
    width: 16px;
    margin-right:6px;
    margin-bottom:4px;
  }

  .new_post {
    position:sticky;
    top:70px;
    float:right;
    margin-right:20px;
    width:250px;
  }

  @media (max-width:900px) {
    .new_post {
      position:absolute;
      justify-content: center;
      width:85%;
      max-width:400px;
      top: 150px;
      left: auto;
      right:auto;
      float:none;
      margin-left:15px;
    }
  }

</style>