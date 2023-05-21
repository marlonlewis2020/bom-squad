<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import OrderForm from '../components/OrderForm.vue'
  import TheOrders from '../components/TheOrders.vue'
  // import TheSchedule from '../components/TheSchedule.vue'
  import TruckForm from '../components/TruckForm.vue'
  import TheRegister from '../components/TheRegister.vue'
  
  let id:number  = Number(localStorage['id']);
  
  let order_url:string = `/api/v1/orders`;
  let orders = ref([]);

  let page_orders = ref([]);
  let perPage = 5;
  let page = ref(1);
  let total = ref(0);
  let final_page = ref(1);
  
  onMounted(() => {

    fetch(order_url, {headers:{
      // Authorization: `bearer ${localStorage['token']}`
    }})
    .then((result) => result.json())
    .then((json_result) => {
      if (json_result.status=="success") {
        orders.value = json_result.data;
        total.value = orders.value.length;
        final_page.value = Math.ceil(total.value/perPage);
        updatePage(1);
      }
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
    
  }

  function updateStatus() {
    
  }

  function cancelOrder() {

  }

  function close() {
    $("[data-dismiss=modal]").trigger({ type: "click" });
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
  }

</script>

<template>
  <main>
    <div class="container">
      <div class="buttons">

        <button 
          v-if="id" 
          @click="clear"
          type="button" 
          value="New Order" 
          class="admin text-center btn btn-primary" 
          data-toggle="modal" 
          data-target="#addordermodal">
          New Order
        </button>

        <button 
          v-if="id" 
          @click="clear"
          type="button" 
          value="New Customer" 
          class="admin text-center btn btn-dark" 
          data-toggle="modal" 
          data-target="#addcustomermodal">
          New Customer
        </button>

        <button 
          v-if="id" 
          @click="clear"
          type="button" 
          value="New Truck" 
          class="admin text-center btn btn-info" 
          data-toggle="modal" 
          data-target="#addtruckmodal">
          New Truck
        </button>
      </div>

      <div class="row">
      
        <TheOrders id="orders" 
        :orders="page_orders"
        :page="page"
        :perPage="perPage"
        :final_page="final_page"
        @cancel="cancelOrder"
        @update="updateStatus"
        @view="viewOrder" 
        @updatePage="updatePage"
        @close="close"/>   

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
      <div class="row">
        <!-- <TheSchedule /> -->
      </div>
    </div>
  </main>
</template>

<style scoped>

  .buttons {
    position:sticky;
    top:60px;
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