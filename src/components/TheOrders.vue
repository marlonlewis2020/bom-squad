<template>
    <div class="table">
        <h1>Orders</h1>
        <table class="table-striped table-bordered table-hover">
            <thead>
                <th>ID</th>
                <th>Customer</th>
                <!-- <th>Parish</th> -->
                <th>Date</th>
                <th>Time</th>
                <!-- <th>Total</th> -->
                <th>87</th>
                <th>90</th>
                <th>Diesel</th>
                <th>ULSD</th>
                <th>status</th>
                <th>Actions</th>
            </thead>
            <tbody>
                <tr :id="order['orderID']" v-for="(order, index) in orders" 
                    :order="order"
                    :key="index"> 
                    <td>{{ order['orderID'] }}</td>
                    <td>{{ order['customerName'] }}</td>
                    <!-- <td>{{ order['parish'] }}</td> -->
                    <td>{{ (order['deliveryDate']) }}</td>
                    <td>{{ order['deliveryTime'] }}</td>
                    <!-- <td>{{ order['orderQuantity'] }}</td> -->
                    <td>{{ order['q_87'] }}</td>
                    <td>{{ order['q_90'] }}</td>
                    <td>{{ order['q_diesel'] }}</td>
                    <td>{{ order['q_ulsd'] }}</td>
                    <td><select name="status" id="status">
                        <option value="" disabled></option>
                        <option :value="order['status']" selected>{{ order['status'] }}</option>
                        <option value="pending" v-if="order['status']!=='Pending' && order['status']!=='Delivered'">Pending</option>
                        <option value="ready" v-if="order['status']!=='Ready' && order.status!=='Delivered'">Processing</option>
                        <option value="preparing" v-if="order['status']!=='Preparing' && order['status']!=='Delivered'">Preparing</option>
                        <option value="delivering" v-if="order['status']!=='Pending' && order['status']!=='Delivering' && order['status']!=='Delivered'">Out for Delivery</option>
                        <option value="delivered" v-if="order['status']!=='Pending' && order['status']!=='Processing' && order['status']!=='Delivered'">Delivered</option>
                    </select></td>
                    <td :id="order['orderID']+`_actions`">
                        <div class="action_button btn btn-primary" @click="view(order['orderID'])"> View</div>
                        <div class="action_button btn btn-primary" @click="update(order['orderID'])"> Update</div>
                        <div class="action_button btn btn-dark" @click="cancel(order['orderID'])"> Cancel</div>
                    </td> 
                </tr>
            </tbody>
        </table>
        <nav aria-label="Page navigation">
          <ul class="pagination justify-content-center">

            <li v-if="page>1" class="page-item page-link" @click="back" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
              
            </li>

            <li v-if="page>1" class="page-item page-link" @click="back"><span>{{ page - 1 }}</span></li>
            <li class="page-item active"><strong>&nbsp;&nbsp;&nbsp;{{ page }}&nbsp;&nbsp;&nbsp;</strong></li>
            <li v-if="page<final_page" class="page-item page-link" @click="next"><span>{{ page + 1 }}</span></li>
            
            <li class="page-item page-link"
                v-if="page<final_page"
                @click="next" 
                aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </li>

          </ul>
        </nav>
    </div>

</template>


<script setup lang="ts">
    // import { ref, onMounted } from 'vue'

    const prop = defineProps(['orders', 'page', 'perPage', 'final_page']);
    const emit = defineEmits<{
        (event:'view', id:number): void;
        (event:'update', id:number, status:string): void;
        (event:'cancel', id:number): void;
        (event:'updatePage', page:number): void;
    }>();

    // onMounted(() => {
        
    // })

    function back() {
        let prev = prop.page-1;
        emit('updatePage', prev);
        // location.reload();
    }

    function next() {
        let nex = prop.page+1;
        emit('updatePage', nex);
        // location.reload();
    }

    function update(id:number, status:string){
        emit('update', id, status);
    }

    function cancel(id:number){
        emit('cancel', id);
    }

    function view(id:number){
        emit('view', id);
    }
</script>


<style scoped>

  input[type="file"] {
    width: 110px;
    border: none;
    background-color: none;
  }

  .active {
    margin-top:6px;
  }

  li:hover{
    cursor:pointer;
  }

  .action_button {
    width:75px;
    margin-bottom:10px;
  }

  .table {
    width:690px;
  }

  thead {
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
</style>