<template>

    <div>
        <h5>Today's Schedule</h5>
        <div class="table">
            <table class="table-striped table-hover table-bordered">
                <thead>
                    <th>ID</th>
                    <th class="main-content">License</th>
                    <th class="main-content">Filled</th>
                    <th class="main-content">Available</th>
                    <th class="main-content">Time</th>
                    <th class="main-content">Actions</th>
                </thead>
                <tbody>
                    <tr v-for="(delivery, index) in deliveries" :key=index v-if="moment.parseZone(delivery_date).format('MMMM DD, YYYY')==day">
                        <td style="width:fit-content">{{delivery['id']}}</td>
                        <td>{{delivery['license_plate']}}</td>
                        <td>{{delivery['filled']}}</td>
                        <td>{{delivery['available']}}</td>
                        <td>{{delivery['time']}}</td>
                        <td>
                            <button type="button" class="btn btn-primary">Orders</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="modal-forms">
            <!-- Add Order Modal -->
            <div id="deliveryordersmodal" class="modal fade">
                <div class="modal-dialog">
                    <!-- <DeliveryOrders /> -->
                </div>
            </div>
        </div> 
    </div>

</template>

<script setup lang="ts">
    import moment from 'moment';

    const emit = defineEmits<{
        (event:'refresh'):void
    }>();
    const prop = defineProps(['deliveries']);
    const today = moment(Date()).format('MMMM DD, YYYY');
    const tomorrow = moment(Date()).add(1,'days').format('MMMM DD, YYYY');
    var day = today;

    function to_today() {
        day=today;
        refresh();
    }

    function to_tomorrow() {
        day=tomorrow;
        refresh();
    }

    function refresh() {
        // this.$forceUpdate();
        console.log("refreshed");
    }
</script>

<style>
    .main-content {
        width:90px;
    }

    thead {
        background-color:rgb(89, 89, 152);
        color:aliceblue;
    }

    table {
        width:fit-content; 
        overflow:scroll; 
        max-height:400px;
    }

    .day {
        margin-left:15px;
        margin-bottom:15px;
        padding:6px 10px;
        color:aliceblue;
        box-shadow:1px 1px 1px gray;
        border:none;
    }
</style>