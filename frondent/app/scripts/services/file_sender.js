'use strict';

/**
 * @ngdoc service
 * @name mmmApp.fileSender
 * @description
 * # fileSender
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('FileSender', ['url','auth','$state',function (url,auth,$state) {
    var data;
    function createFormData(){
      data = new FormData();
      data.append('id',auth.id);
      data.append('access_token',auth.access_token)
    }
    return {
      load:function(object){
        createFormData();
        for(var prop in object){
          if(object.hasOwnProperty(prop)){
            data.append(prop,object[prop])
          }
        }
      },
      add:function(object){
        for(var prop in object){
          if(object.hasOwnProperty(prop)){
            data.append(prop,object[prop])
          }
        }
      },
      send:function(){
        var xhr = new XMLHttpRequest();
        xhr.open('post',url.upload);
        xhr.onreadystatechange = function(){
          if(xhr.readyState == 4 ){
            console.log(xhr.responseText);
            $state.reload('dashboard.fund_management')
          }
        };
        xhr.send(data)
      }
    };
  }]);
