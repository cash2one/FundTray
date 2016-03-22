'use strict';

/**
 * @ngdoc service
 * @name mmmApp.registerCache
 * @description
 * # buffer 跨scope存储的对象
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('buffer', function () {
    var buffer = {};
    return {
      set:function(object){
        if(angular.isObject(object)){
            angular.extend(buffer,object);
        }
      },
      get:function(){return buffer;},
      clear:function(){buffer={}}
    };
  });
