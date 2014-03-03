function firebase () {
 

  firebase.prototype.insert=function(object1,type1,callback) {
  var serializedData2 ='object='+object1+'&type='+type1;
  alert(serializedData2);
  $.ajax({
    type: 'post',
    url: 'http://localhost:8000/insert',
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
      url: 'http://localhost:8000/query',
      data: 'Id1='+queryId,
      async:true,
      success: callback,
      error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
      }
    });
}

firebase.prototype.search=function(key1,gle2,value1,parameter1,gle1,parameterValue1,limit1,callback) {
  var serializedData2 = 'key1='+key1+'&gle2='+gle2+'&value1='+value1+'&parameter1='+parameter1+'&gle1='+gle1+'&parameterValue1='+parameterValue1+'&limit1='+limit1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/search',
        data: serializedData2,
        async:true,
        success: callback,
      error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
      }
    });
}
firebase.prototype.removeObj=function (removeId1,callback) {
  var serializedData2 = 'removeId1='+removeId1;
    $.ajax({
        type: 'post',
        url: 'http://localhost:8000/remove',
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
        url: 'http://localhost:8000/indexKey',
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
        url: 'http://localhost:8000/publish',
        data: serializedData2,
        async:true,
        success: callback,
        error: function(XMLHttpRequest, textstatus, error) { 
          console.log(error);         
        }
     });
}
firebase.prototype.subscribe=function(subscribeChannel1,subscribeLimit1,callback) {
  var serializedData = 'subscribeChannel1='+subscribeChannel1+'&subscribeLimit1='+subscribeLimit1;
    $.ajax({
        type: 'post',
      url: 'http://localhost:8000/subscribe',
      data: serializedData,
      success: callback,
      error: function(XMLHttpRequest, textstatus, error) { 
        console.log(error);         
      }   
    });
}
}
