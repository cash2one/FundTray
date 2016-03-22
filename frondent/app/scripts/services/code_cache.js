'use strict';

/**
 * @ngdoc service
 * @name mmmApp.codeCache
 * @description
 * # codeCache
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('codeCache', function () {
    var code;
    return {
      set:function(data){
        code = data;
      },
      verify:function(data){
          if(angular.isString(data)){
              return code.toLowerCase() == data.toLowerCase();
          }
          return false
      },
      get:function(){
          return code;
      }
    };
  });
