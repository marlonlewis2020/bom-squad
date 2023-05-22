<template>
    <form method="POST" action="" >
        <div class="form-group">
            <span><small><em>Order No: {{ order['orderID'] }}</em></small></span>
        </div>
        <div class="form-group">
            <label for="cus_name">Customer</label>
            <input class="form-control" id="cus_name" type="text" name="cus_name" :value="order['customerName']" disabled>
            <label for="address">Address</label>
            <textarea class="form-control" id="address" type="text" name="address" disabled>{{ order['address'] }}</textarea>
        </div>
        <div class="form-group petrol-group">
            <span class="petrol">
                <label for="diesel">Diesel Quantity:</label>
                <input class="field form-control" id="diesel" type="number" name="diesel" :value="order['q_diesel']" disabled>
            </span>

            <span class="petrol">
                <label for="87">87 Quantity:</label>
                <input class="field form-control" id="87" type="number" name="87" :value="order['q_87']" disabled>
            </span>

            <span class="petrol">
                <label for="90">90 Quantity:</label>
                <input class="field form-control" id="90" type="number" name="90" :value="order['q_90']" disabled>
            </span>

            <span class="petrol">
                <label for="ulsd">ULSD Quantity:</label>
                <input class="field form-control" id="ulsd" type="number" name="ulsd" :value="order['q_ulsd']" disabled>
            </span>
        </div>
        <div class="form-group buttons text-center">
            <!-- <button type="button" value="Edit">Edit</button> -->
            <button class="btn btn-danger btn-close" type="button" data-dismiss="modal" aria-label="Close" value="Close">Close</button>
        </div>
    </form>
</template>

<script setup lang="ts">

    const prop = defineProps(['order']);
    const emit = defineEmits<{
        (event:'cancel'):void
        (event:'update'):void
    }>();

</script>

<style scoped>
    .petrol-group {
        display: grid;
        grid-template-columns:1fr 1fr;
    }

    .field {
        width:30%;
        float:right;
        margin-right:30px;
        margin-bottom: 15px;
    }

</style>