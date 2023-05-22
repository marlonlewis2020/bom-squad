<template>
    <div class="table">
        <h1>Orders</h1>
        <table class="table-striped table-bordered table-hover">
            <thead>
                <th>ID</th>
                <th>Customer</th>
                <th>Date</th>
                <th>Time</th>
                <th>Total(L)</th>
                <th>status</th>
                <th style="width:85px;">Actions</th>
            </thead>
            <tbody>
                <tr v-for="(order, index) in orders" 
                    :key="index"> 
                    <td>{{ order['orderID'] }}</td>
                    <td>{{ order['customerName'] }}</td>
                    <td>{{ moment.parseZone(order['deliveryDate']+'+05:00').format('MMMM DD, YYYY') }}</td>
                    <td>{{ order['deliveryTime'] }}</td>
                    <td>{{ order['orderQuantity'] }}</td>
                    <td><select name="status" id="status">
                        <option value="" disabled></option>
                        <option :value="order['status']" selected>{{ order['status'] }}</option>
                        <option value="pending" v-if="order['status']!=='Pending' && order['status']!=='Delivered'">Pending</option>
                        <option value="ready" v-if="order['status']!=='Ready' && order.status!=='Delivered'">Processing</option>
                        <option value="preparing" v-if="order['status']!=='Preparing' && order['status']!=='Delivered'">Preparing</option>
                        <option value="delivering" v-if="order['status']!=='Delivered'">Out for Delivery</option>
                        <option value="delivered" v-if="order['status']=='Delivering' && order['status']=='Delivered'">Delivered</option>
                    </select></td>
                    <td :id="order['orderID']+`_actions`">
                        <input type="button" 
                        value="View" 
                        class="action_button btn btn-primary" 
                        @click="view(index)" 
                        data-toggle="modal" 
                        data-target="#viewordermodal"> 
                        <input type="button" value="Update" class="action_button btn btn-primary" @click="update(order['orderID'])" disabled> 
                        <input type="button" value="Cancel" class="action_button btn btn-dark" @click="cancel(order['orderID'])" disabled> 
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
    
    <div class="modal-forms">
      <!-- Add Order Modal -->
      <div id="viewordermodal" class="modal fade">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class='modal-header'>
              <h5> View Order </h5>
              <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="close" >x</button>
            </div>
            <div class=modal-body>
              <SingleOrder :order="this_order" @close="close" />
            </div>
          </div>
        </div>
      </div>
    </div> 

</template>


<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import moment from 'moment-timezone';
    import SingleOrder from '../components/SingleOrder.vue';

    let this_order = ref({});

    const prop = defineProps(['orders', 'page', 'perPage', 'final_page']);
    const emit = defineEmits<{
        (event:'view', id:number): void;
        (event:'update', id:number, status:string): void;
        (event:'cancel', id:number): void;
        (event:'updatePage', page:number): void;
        (event:'close'): void;
        (event:'refresh'): void;
    }>();

    onMounted(() => {
      console.log(moment("Sat, 27 May 2023 00:00:00 GMT"));
    });

    function back() {
        let prev = prop.page-1;
        emit('updatePage', prev);
    }

    function next() {
        let nex = prop.page+1;
        emit('updatePage', nex);
    }

    function update(id:number, status:string){
        emit('update', id, status);
    }

    function cancel(id:number){
        emit('cancel', id);
    }

    function view(index:number){
        this_order.value = prop.orders[index];
    }

    function close() {
      $("[data-dismiss=modal]").trigger("click");
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
    width:fit-content;
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