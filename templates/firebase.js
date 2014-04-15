function firebase () {

  firebase.prototype.insert=function(object1,type1,callback) {
  var serializedData2 ='object='+object1+'&type='+type1;
  $.ajax({
    type: 'post',
    url: 'http://localhost:8002/insert',
    data: serializedData2,
    async:true,
    success: callback,
    error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }
  });
}  
  firebase.prototype.query=function (queryId,callback) {
    $.ajax({
      type: 'post',
      url: 'http://localhost:8002/query',
      data: 'Id1='+queryId,
      async:true,
      success: function(data){
        //alert(data);
        json_obj=JSON.parse(data);
        callback(json_obj);
      },
      error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
      }
    });
}

firebase.prototype.search=function(argumentsObj,callback) {
  
  var key1 = argumentsObj.key1;
  var gle2 = argumentsObj.gle2;
  var value1 = argumentsObj.value1;
  // var parameter1 = argumentsObj.parameter1;
  // var gle1 = argumentsObj.gle1;
  // var parameterValue1=argumentsObj.parameterValue1;
  // var limit1=argumentsObj.limit1;
  if(typeof(limit1)==='undefined'){
   limit1='*';
  }
  if(typeof(parameter1)==='undefined'){
   parameter1='Timestamp';
   gle1='>';
   parameterValue1='0';
  }
  alert(parameter1+gle1+parameterValue1);
  var serializedData2 = 'key1='+key1+'&gle2='+gle2+'&value1='+value1+'&parameter1='+parameter1+'&gle1='+gle1+'&parameterValue1='+parameterValue1+'&limit1='+limit1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/search',
        data: serializedData2,
        async:true,
        success: function(data){
        var json_obj=JSON.parse(data);
        callback(json_obj);
      },
      error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
      }
    });
}
firebase.prototype.removeObj=function (removeId1,callback) {
  var serializedData2 = 'removeId1='+removeId1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/remove',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}


firebase.prototype.indexKey=function (index1,type1,callback) {
  var serializedData2 = 'index1='+index1+'&type1='+type1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/indexKey',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}
firebase.prototype.publish=function (publishObject1,publishChannel1,callback) {
  var serializedData2 = 'publishObject1='+publishObject1+'&publishChannel1='+publishChannel1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/publish',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(textstatus);         
        }
     });
}
firebase.prototype.subscribe=function(subscribeChannel1,subscribeLimit1,timestamp,session,callback) {

  var serializedData = 'subscribeChannel1='+subscribeChannel1+'&subscribeLimit1='+subscribeLimit1+'&timestamp='+timestamp+'&session='+session;
  //alert(session);
    $.ajax({
        type: 'post',
      url: 'http://localhost:8002/subscribe',
      data: serializedData,
      async:true,
      success: function (data){
         var json_obj=JSON.parse(data);
       //alert(data);
         callback(json_obj);
         var timestamp=json_obj[0].Timestamp;
        setTimeout('firebase.prototype.subscribe("'+subscribeChannel1+'","'+subscribeLimit1+'","'+timestamp+'","'+session+'",'+callback+')',100);
         },
      error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }   
    });
}

firebase.prototype.removeps=function (removeChannel1,rankStart1,rankEnd1,callback) {
  var serializedData2 = 'removeChannel1='+removeChannel1+'&rankStart1='+rankStart1+'&rankEnd1='+rankEnd1;

    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/removeps',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(textstatus);         
        }
     });
}

firebase.prototype.removepsbykey=function (removeChannel1,key,callback) {
var serializedData2 = 'removeChannel1='+removeChannel1+'&key='+key;

    $.ajax({
        type: 'post',
        url: 'http://localhost:8002/removepsbykey',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(textstatus);         
        }
     });
}
}