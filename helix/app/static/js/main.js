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
        if ($(this).val() == "y"){
          $(this).val("n")
          if ($('#type').val() == "lwm2m") {
            $('#port').val('5683');
          }
          if ($('#type').val() == "mqtt") {
            $('#port').val('1883');
          }
        }
        else {
          $(this).val("y")
          if ($('#type').val() == "lwm2m") {
            $('#port').val('5684');
          }
          if ($('#type').val() == "mqtt") {
            $('#port').val('8883');
          }
        }
      }
    );
});

function observer () {
  if (window.blurred) { return; }
  if( window.location.pathname == "/admin/agents"){
    window.location = "/admin/agents"
  }
  if( window.location.pathname == "/admin/brokers"){
    window.location = "/admin/brokers"
  }
}

(function() {
    var time = 10000,
        delta = 100,
        tid;
    tid = setInterval(function() {
        if ( window.blurred ) { return; }
        time -= delta;
        if ( time <= 0 ) {
            clearInterval(tid);
            observer()
        }
    }, delta);
})();

window.onblur = function() { window.blurred = true; };
window.onfocus = function() { window.blurred = false; };

$("#type").val("lwm2m").trigger('change');
$("#type").val("mqtt").trigger('change');
