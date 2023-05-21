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
                  <input type="text" name="license_plate" id="license_plate" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                  <label for="capacity">Compartments &nbsp;<small style="font-size:10px;">( i.e. 80,20,50,40 )</small></label>
                  <input type="text" name="capacity" id="capacity" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                
                <div class="form-group">
                    <label for="model">Model</label>
                    <input type="text" name="model" id="model" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                    <label for="make">Make</label>
                    <input type="text" name="make" id="make" cols="30" rows="2" class="form-control" maxlength="75" required>
                </div>
                <div class="form-group">
                  <label for="year">Year</label>
                  <input type="number" name="year" id="year" cols="30" rows="2" class="form-control" maxlength="75" required>
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

    const emit = defineEmits<{
        (event:'close'):void
    }>()
    
    let id  = Number(localStorage['id']);
    let role = 'admin';
    
    let url = `/api/v1/trucks`;


    function addTruck() {
        let error_highlight = 'rgb(175, 95, 95)';
        let error_weight = 'bold';
        if (id && typeof id == 'number' && license_plate.value!=="" && $('#capacity').val()!=="" && $('#year').val()!==0 && $('#make').val()!==""  && $('#model').val()!=="") {
            console.log("Create Truck function called");
            console.log($('form#createTruckForm')[0]);

            fetch(url, {
                method: 'POST',
                headers: {},
                body: new FormData($('form#createTruckForm')[0])
            })
            .then((result)=>{
                return result.json();
            })
            .then((data)=>{
                if (data.status == "success") {
                    console.log("Truck added successfully");
                    alert("Truck added successfully");
                    console.log(data);
                } else {
                    console.log(data);
                }
                emit('close');
            });
        } else {
            alert("Form is invalid.");
            if ($('#license_plate').val()==""){
                $('#license_plate').css({'background-color':error_highlight});
                $('#license_plate').css({'font-weight':error_weight});
            }
            if ($('#capacity').val()==""){
                $('#capacity').css({'background-color':error_highlight});
                $('#capacity').css({'font-weight':error_weight});
            }
            if ($('#year').val()==0){
                $('#year').css({'background-color':error_highlight});
                $('#year').css({'font-weight':error_weight});
            }
            if ($('#make').val()==""){
                $('#make').css({'background-color':error_highlight});
                $('#make').css({'font-weight':error_weight});
            }
            if ($('#model').val()==""){
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
        $('#license_plate').val("");
        $('#capacity').val("");
        $('#model').val("");
        $('#make').val("");
        $('#year').val(0);
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