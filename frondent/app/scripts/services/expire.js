'use strict';

/**
 * @ngdoc service
 * @name mmmApp.expire
 * @description
 * # expire
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('expire', ['$timeout','$interval',function ($timeout,$interval) {
    var cache_ls = [],promise;

    function updateOne(item){
        var now = parseInt(+ new Date()/1000);
        item.expire_time = parseInt(item.apply_mtime) - now  + 60*60*24;
    }
    function updateAll(){
        var func;
        for (var index= 0,len = cache_ls.length;index<len;index++){
            func = cache_ls[index];
            func.apply(null,[]);
        }
    }
    function cycle(){
        promise =  $interval(updateAll,1000)
    }
    function clear(){
        $interval.cancel(promise);
        cache_ls = []
    }
    function addExpire(ls){
        var item;
        for(var index= 0,len=ls.length;index<len;index++){
            item = ls[index];
            if(item.apply_stime){
                updateOne(item);
                cache_ls.push(function(item){
                    return function (){
                        updateOne(item);
                        console.log(item);
                    }
                }(item))
            }
        }
        return ls
    }
    return {
        add:addExpire,
        cycleAll:cycle,
        clearAll:clear
    };
  }]);
