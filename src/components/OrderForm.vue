<template>
    <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title" id="modalLabel"> Place Order</h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" >x</button>
      </div>
      <div class="modal-body">
          <form id="createOrderForm" action="" method="post" enctype="multipart/form-data">
              <div class="form-group">
                  <div class="form-group" v-if="role='admin'">
                      <label>Select Customer</label>
                      <select name="customer" id="select_customer" @change="updateCustomer" class="form-control">
                          <option></option>
                          <option 
                              v-for="(customer, index) in customers" 
                              :value="customer['customerID']" 
                              :key='index' > {{ customer['company'] }} - {{ customer['branch'] }} </option>
                      </select>
                      <input name="customer_id" :value="customer_id" id="customer_id" cols="30" rows="2" class="form-control" maxlength="75" hidden>
                  </div>
                <div class="form-group">
                  <label for="delivery_date">Delivery Date</label>
                  <input v-model="delivery_date" type="date" name="delivery_date" id="delivery_date" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                  <label for="delivery_time">Delivery Time</label>
                  <select name="delivery_time" id="delivery_time" cols="30" rows="2" class="form-control" maxlength="75" required>
                    <option value="Early" selected>Early</option>
                    <option value="Late">Late</option>
                  </select>
                </div>
                <div class="form-group" hidden>
                  <label for="quantity">Quantity</label>
                  <input v-bind:value="quantity" name="quantity" id="quantity" cols="30" rows="2" class="form-control" maxlength="75" v-on:change="change">
                </div>
                <div class="form-group">
                  <label for="q_diesel">Diesel</label>
                  <input v-model="q_diesel" type="number" @change="updateQuantity" name="q_diesel" id="q_diesel" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group">
                  <label for="q_87">87</label>
                  <input v-model="q_87" type="number" @change="updateQuantity" name="q_87" id="q_87" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group">
                  <label for="q_90">90</label>
                  <input v-model="q_90" type="number" @change="updateQuantity" name="q_90" id="q_90" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group">
                  <label for="q_ulsd">ulsd</label>
                  <input v-model="q_ulsd" type="number" @change="updateQuantity" name="q_ulsd" id="q_ulsd" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group" hidden>
                  <label for="price">Price</label>
                  <input value="0.00" type="decimal" name="price" id="price" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group" hidden>
                  <label for="status">Status</label>
                  <input value="Pending" name="status" id="status" cols="30" rows="2" class="form-control" maxlength="75" hidden>
                </div>
                <div class="form-group" hidden>
                  <label for="location" >Address</label>
                  <input :value="cx['address_id']" type="text" name="location" id="location" cols="30" rows="2" class="form-control" maxlength="75">
                </div>
                <div class="form-group">
                  <label for="preferred">Preference</label>
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
            class="btn btn-info"
            @click="clear" >
              Clear
          </button>
          <button 
            type="button" 
            class="btn btn-secondary"
            @click="close" 
            data-dismiss="modal">
              Close
          </button>
      </div>
    </div>
</template>

<script setup lang='ts'>

    import { ref, onMounted } from 'vue';
    let role = 'admin';

    let id  = Number(localStorage['id']);
    let customers = ref([]);
    
    let url = `/api/v1/customers/all`;
    let delivery_date = ref("");
    let delivery_time = ref("");
    let quantity = 0;
    let q_diesel = ref(0);
    let q_87 = ref(0);
    let q_90 = ref(110);
    let q_ulsd = ref(0);
    let preferred = ref("90");
    let location = ref("");
    let cx = ref({});
    let customer_id = ref(0);

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
                customers.value = data.data;
            } else {
            console.log(data.message);
            }
        });
    });

    const emit = defineEmits<{
        (event:'close'): void
        (event:'change'): void
        (event:'refresh'): void
    }>();

    function updateCustomer(event) {
        let options = event.target;
        let selected_index = options.selectedIndex - 1;
        if (selected_index > -1) {
            cx.value = customers.value[selected_index];
            customer_id = cx.value['customer_id'];
            console.log(cx.value);
        }
    }

    function addOrder() {
        let error_highlight = 'rgb(175, 95, 95)';
        let error_weight = 'bold';
        if (id && typeof id == 'number' && delivery_date.value!=="" && $('#delivery_time').val()!=="" && $('#select_customer').val()!=="") {
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
                    alert("order created successfully");
                    console.log(data);
                    emit('close');
                    emit('refresh');
                } else if(data.status == "unavailable") {
                  console.log("There are no available trucks at this time to fulfill your order.");
                  alert("There are no available trucks at this time to fulfill your order.");
                  console.log(data);
                  emit('close');
                  emit('refresh');
                } else if(data.status == "invalid") {
                  console.log("Your order is invalid. Please try again.");
                  alert("Your order is invalid. Please try again.");
                  console.log(data);
                  emit('close');
                  emit('refresh');
                }
                else {
                    console.log(data);
                    emit('refresh');
                    alert("There are no available trucks. Contact us by phone or email for further assistance or try another date.");
                    emit('close');
                }
            });
        } else {
            alert("Form is invalid.");
            if (delivery_date.value==""){
                $('#delivery_date').css({'background-color':error_highlight});
                $('#delivery_date').css({'font-weight':error_weight});
            }
            if (delivery_time.value==""){
                $('#delivery_time').css({'background-color':error_highlight});
                $('#delivery_time').css({'font-weight':error_weight});
            }
            if ($('#select_customer').val()==""){
                $('#select_customer').css({'background-color':error_highlight});
                $('#select_customer').css({'font-weight':error_weight});
            }
        }
        
        $('.form-control').on('click', function(){
            if ($(this).css('background-color')==error_highlight) {
                $(this).css({'background-color':'white'});
                $(this).css({'font-weight':'normal'});
            }
        });
    }



    function change() {
        emit('change');
    }

    function close() {
        emit('close');
    }

    function clear() {
        delivery_date.value = "";
        delivery_time.value = "";
        quantity = 0;
        q_diesel.value = 0;
        q_87.value = 0;
        q_90.value = 0;
        q_ulsd.value = 0;
        preferred.value = "90";
        location.value = "";
    }

    function updateQuantity() {
        quantity = Number(q_diesel.value) + Number(q_87.value) + Number(q_90.value) + Number(q_ulsd.value);
    }
</script>

<style scoped>

  .modal-header {
    background-color:rgb(89, 89, 152);
    color:aliceblue;
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