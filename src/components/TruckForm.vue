<template>
    <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title" id="modalLabel"> Add Truck</h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" >x</button>
      </div>
      <div class="modal-body">
          <form id="createTruckForm" action="" method="post" enctype="multipart/form-data">
              <div class="form-group">
                <div class="form-group">
                  <label for="license_plate">License Plate No.</label>
                  <input v-model:license_plate="license_plate" type="text" name="license_plate" id="license_plate" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                  <label for="capacity">Compartments (text i.e. 80,20,50,40)</label>
                  <input v-model:capacity="capacity" type="text" name="capacity" id="capacity" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                
                <div class="form-group">
                    <label for="model">Make</label>
                    <input v-model:value="model" type="text" name="model" id="model" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                    <label for="make">Make</label>
                    <input v-model:value="make" type="text" name="make" id="make" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                  <label for="year">Year</label>
                  <input v-model:value="year" type="number" name="year" id="year" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <input name="active" id="active" type="number" value="1" hidden>
            </div>
          </form>
      </div>
      <div class="modal-footer">
          <button type="button" 
            v-on:click="addTruck" 
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
    
    let id  = Number(localStorage['id']);
    let role = 'admin';
    
    let url = `/api/v1/trucks`;
    
    let license_plate = ref("");
    let capacity = ref("");
    let year = ref(0);
    let make = ref("90");
    let model = ref("");

    function addTruck() {
        let error_highlight = 'rgb(175, 95, 95)';
        let error_weight = 'bold';
        if (id && typeof id == 'number' && license_plate.value!=="" && $('#capacity').val()!=="" && $('#year').val()!==0 && $('#make').val()!==""  && $('#model').val()!=="") {
            console.log("Create Truck function called");
            console.log($('form#createTruckForm')[0]);

            fetch("/api/v1/orders", {
                method: 'POST',
                headers: {},
                body: new FormData($('form#createTruckForm')[0])
            })
            .then((result)=>{
                return result.json();
            })
            .then((data)=>{
                if (data.status == "success") {
                    console.log("Truck created successfully");
                    alert("order created successfully");
                    console.log(data);
                } else {
                    console.log(data);
                }
            });
        } else {
            alert("Form is invalid.");
            if (license_plate.value==""){
                $('#license_plate').css({'background-color':error_highlight});
                $('#license_plate').css({'font-weight':error_weight});
            }
            if (capacity.value==""){
                $('#capacity').css({'background-color':error_highlight});
                $('#capacity').css({'font-weight':error_weight});
            }
            if (year.value==0){
                $('#year').css({'background-color':error_highlight});
                $('#year').css({'font-weight':error_weight});
            }
            if (make.value==""){
                $('#make').css({'background-color':error_highlight});
                $('#make').css({'font-weight':error_weight});
            }
            if (model.value==""){
                $('#model').css({'background-color':error_highlight});
                $('#model').css({'font-weight':error_weight});
            }
        }
        
        $('.form-control').on('click', function(){
            if ($(this).css('background-color')==error_highlight) {
                $(this).css({'background-color':'white'});
                $(this).css({'font-weight':'normal'});
            }
        });
    }


    function close() {
        emit('close');
    }


    function clear() {
        license_plate.value = "";
        capacity.value = "";
        year = 0;
        active.value = 1;
        make.value = "";
        model.value = ""
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