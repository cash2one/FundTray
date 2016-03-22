/**
 * Created by Administrator on 2016-2-22.
 */
'use strict';

angular.module('mmmApp')
  .service('AccountMgr', ['url','$q','$http',function (url,$q,$http) {
    var info_dic = {};
    this.info = function(){
      return info_dic;
    };
    this.clear = function(){
      info_dic = {};
    };
    this.init = function(data){
      if(angular.isObject(data)){
        info_dic = data;
      }
    };
  }]);
