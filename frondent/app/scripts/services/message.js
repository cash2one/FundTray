'use strict';

/**
 * @ngdoc service
 * @name mmmApp.noticeCache
 * @description
 * # noticeCache
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('Message', ['$q',function ($q) {
    var inner = {},callbacks=[];
    inner.timestamp = +new Date();
    Object.defineProperty(this,'content',{
      get:function(){
        return inner.timestamp +':'+ (inner.content?inner.content:'');
      },
      set:function(val){
        inner.timestamp = +new Date();
        inner.content = (val?val:'');
      }
    });
    this.show = function(string,level){
      this.content = string;
      this.level = level||0;
    };
    this.hide = function(){this.content = null;};
    this.addCallbacks = function(func){
      var defer = $q.defer(),result;
      if (angular.isFunction(func)){
        var args = Array.prototype.slice.call(arguments,1);
        callbacks.push(function(){
          result = func.apply(null,args);
          try{
            if(result instanceof $q.defer().promise.constructor){
              result.then(
                function(){defer.resolve()},
                function(){defer.reject()}
              )
            }
            // 尝试假设返回promise，如果不是的话，就静默catch失败。
          } catch(error){}
        });
      }
      return defer.promise;
    };
    this.involveCallbacks = function(){
      angular.forEach(callbacks,function(callback){
        callback();
      });
      this.clearCallbacks()
    };
    this.clearCallbacks = function(){callbacks = []};
  }]);
