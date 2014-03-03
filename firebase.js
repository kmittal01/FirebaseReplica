function subscribe() {
  var serializedData = $("#subs").serialize();
    $.ajax({
        type: 'post',
      url: 'http://localhost:8000/subscribe',
      data: serializedData,
      success: function(data) {
        $('#msg').html(data);
        setTimeout('subscribe()', 1000);
      },
      error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }   
    });
}

function insert() {
  var serializedData2 = $("#ins").serialize();
  $.ajax({
    type: 'post',
    url: 'http://localhost:8000/insert',
    data: serializedData2,
    async:true,
    success: function(data) {
      $('#insertReturn').html(data);
      alert(data);
    },
    error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }
  });
}

function search() {
  var serializedData2 = $("#search").serialize();
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/search',
        data: serializedData2,
        async:true,
        success: function(data) {
          $('#searchReturn').html(data);
          alert(data);
        },
      error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
      }
    });
}
function removeObj() {
  var serializedData2 = $("#remove").serialize();
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/remove',
        data: serializedData2,
        async:true,
        success: function(data) {
          $('#removeReturn').html(data);
        },
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}

function indexKey() {
  var serializedData2 = $("#indexKey").serialize();
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/indexKey',
        data: serializedData2,
        async:true,
        success: function(data) {
          $('#indexReturn').html(data);
        },
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}
function publish() {
  var serializedData2 = $("#publish").serialize();
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/publish',
        data: serializedData2,
        async:true,
        success: function(data) {
          $('#publishReturn').html(data);
        },
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}
