
// onload function
$(function() {
  console.log( "window ready!" );
  $('#type').on('change', function(){
    if ($(this).val() == "lwm2m"){
      if ($('#encryption').val() == "y"){
       $('#port').val('5684');
      }
      else if ($('#encryption').val() == "n"){
       $('#port').val('5683');
      }
    }
    else if ($(this).val() == "mqtt"){
      if ($('#encryption').val() == "y"){
       $('#port').val('8883');
      }
      else if ($('#encryption').val() == "n"){
       $('#port').val('1883');
      }
    }
  });
  $('#encryption').on('click', function(){
        alert($(this).val())
        if ($(this).val() == "y"){
          $(this).val("n")
        }
        else {
          $(this).val("y")
        }
      }
    );
});



$("#type").val("lwm2m").trigger('change');
$("#type").val("mqtt").trigger('change');
