<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import OrderForm from '../components/OrderForm.vue';
  import TheOrders from '../components/TheOrders.vue';
  import TheSchedule from '../components/TheSchedule.vue';
  import TruckForm from '../components/TruckForm.vue';
  import TheRegister from '../components/TheRegister.vue';
  
  import moment from 'moment';
  moment().tz("America/Los_Angeles").format();
  let id:number  = Number(localStorage['id']);
  
  let order_url:string = `/api/v1/orders`;
  let orders = ref([]);

  let deliveries = ref([]);
  const deliveries_url = '/api/v1/deliveries';

  let page_orders = ref([]);
  let perPage = 5;
  let page = ref(1);
  let total = ref(0);
  let final_page = ref(1);
  let trucks = ref([]);
  let av_truck_date = ref(moment().format('DD/MM/YYYY'));
  let av_truck_time = ref("Early");

  $('body').on('click', '#av_trucks_update', function(){
    fetch('/api/v1/trucks/available', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        'date': av_truck_date.value,
        'time': av_truck_time.value
      })
    })
    .then((response)=>response.json())
    .then((result)=>{
      if (result.status=='success') {
        trucks.value = result.data
      }
    })
  });
  
  onMounted(() => {

    fetch(order_url, {headers:{
      // Authorization: `bearer ${localStorage['token']}`
    }})
    .then((result) => result.json())
    .then((json_result) => {
      if (json_result.status=="success") {
        orders.value = json_result.data;
      }
    })
    .then(()=>{
        total.value = orders.value.length;
        final_page.value = Math.ceil(total.value/perPage);
        updatePage(1);
    });

    fetch(deliveries_url, {
        method: "POST",
        headers: {
            // Authorization: `bearer ${localStorage['token']}`,
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({date:moment(Date()).format('MMMM DD, YYYY')})
    })
    .then((response) => response.json())
    .then((data) => {
        deliveries.value = data.data;
    });
  });

  function updatePage(new_page) {
    page.value = new_page
    const startIndex = perPage * (new_page - 1);
    const endIndex = startIndex + perPage;
    page_orders.value = orders.value.slice(startIndex, endIndex);
    console.log(page_orders);
  }

  function viewOrder() {
    //
  }

  function updateStatus() {
    //
  }

  function cancelOrder() {
    //
  }

  function close() {
    $("[data-dismiss=modal]").trigger("click");
    // location.reload();
  }

  function refresh() {
    fetch(order_url, {headers:{
      // Authorization: `bearer ${localStorage['token']}`
    }})
    .then((result) => result.json())
    .then((json_result) => {
      if (json_result.status=="success") {
        orders.value = json_result.data;
        total.value = orders.value.length;
        final_page.value = Math.ceil(total.value/perPage);
        updatePage(page.value);
      }
    });

    fetch(deliveries_url, {
        method: "POST",
        headers: {
            // Authorization: `bearer ${localStorage['token']}`,
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({date:moment(Date()).format('MMMM DD, YYYY')})
    })
    .then((response) => response.json())
    .then((data) => {
        deliveries.value = data.data;
    });
  }

</script>

<template>
  <main>
    <div class="container-fluid">
      <div class="buttons">

        <button 
          v-if="id" 
          type="button" 
          value="New Order"
          class="admin text-center btn btn-primary" 
          data-toggle="modal" 
          data-target="#addordermodal">
          New Order
        </button>

        <button 
          v-if="id" 
          type="button" 
          value="New Customer" 
          class="admin text-center btn btn-dark" 
          data-toggle="modal" 
          data-target="#addcustomermodal">
          New Customer
        </button>

        <button 
          v-if="id" 
          type="button" 
          value="New Truck" 
          class="admin text-center btn btn-info" 
          data-toggle="modal" 
          data-target="#addtruckmodal">
          New Truck
        </button>

        <div class="form-group">
          <form action="" method="POST">
            <label for="delivery_time"><strong>Available Trucks</strong></label>
            <input :value="av_truck_date" type="date" name="" class="av_period" id="av_truck_date" :min="moment().format('DD/MM/YYYY')">
            <select :value="av_truck_time" name="delivery_time" id="delivery_time" cols="30" rows="2" class="form-control av_period" maxlength="75" required>
              <option value="Early" selected>Early</option>
              <option value="Late">Late</option>
            </select>
            <button type="button" id="av_trucks_update" class="btn-success" style="margin:5px 30px;border-radius:5px;">Check</button>
          </form>
          <small>(view available trucks</small>
          <small> by date)</small>
        </div>
        <div class="av_trucks">
          <div v-for="truck in trucks">
            ID:#{{ truck['id'] }}<br/>
            Capacity : {{ truck['capacity'] }}
          </div>
        </div>
      </div>

      <div class="row">
        
        <div v-if="!orders.length" class="placeholder">
          <h3>Welcome to the Truck Scheduling App</h3>
          <small>Getting Started:</small>
          <p style="margin-left:50px;">
            Step 1: 
            <span class=" text-danger">
              <strong><em>Add Truck</em></strong>
            </span>
            <br/>
            Step 2: 
            <span class=" text-danger">
              <strong><em>Add Customer</em></strong>
            </span>
            <br/><br/><br/><br/>
          </p>
          <small>Main Features:</small><br/>
          <span class=" text-primary" style="margin-left:50px;">
            <strong>Create Order</strong>
          </span>
          
          <span class=" text-primary" style="margin-left:50px;">
            <strong>View/Update Orders</strong>
          </span>
          
          <span class=" text-primary" style="margin-left:50px;">
            <strong>View Schedule</strong>
          </span>
        </div>
        <div class="dashboard-tables">

          <div id='schedule' class="row row-component">
            <TheSchedule :deliveries="deliveries"/>
          </div>

          <div class="row row-component">
            <TheOrders id="orders" 
            v-if="orders.length"
            :orders="page_orders"
            :page="page"
            :perPage="perPage"
            :final_page="final_page"
            @cancel="cancelOrder"
            @update="updateStatus"
            @view="viewOrder" 
            @updatePage="updatePage"
            @close="close"/>   
          </div>

          <div class="modal-forms">
            <!-- Add Order Modal -->
            <div id="addordermodal" class="modal fade">
              <div class="modal-dialog">
                  <OrderForm @close="close" @refresh="refresh" />
              </div>
            </div>
      
            <!-- Add Customer Modal -->
            <div id="addcustomermodal" class="modal fade">
              <div class="modal-dialog">
                  <TheRegister @close="close" />
              </div>
            </div>
    
            <!-- Add Truck Modal -->
            <div id="addtruckmodal" class="modal fade">
              <div class="modal-dialog">
                  <TruckForm @close="close" />
              </div>
            </div>
          </div> 

        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

  #schedule {
    margin-bottom:30px;
  }

  #av_truck_date {
    width:120px;
  }

  .dashboard-tables {
    /* margin-top:30px; */
    margin-left:180px;
    display:flex;
    flex-direction:column;
  }

  .row-component, .placeholder {
    width:100%;
  }

  .placeholder {
    margin-bottom:30px;
  }

  .buttons {
    position:fixed;
    float:left;
    margin-right:20px;
    width:120px;
  }

  .admin {
    width:100%;
    margin-bottom:6px;
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