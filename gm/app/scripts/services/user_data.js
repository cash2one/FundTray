'use strict';

/**
 * @ngdoc service
 * @name mmmApp.userInfo
 * @description
 * # userInfo
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('UserData', ['url','$q','$http','Message',function (url,$q,$http,Message) {
    var user = {};
    this.get = function(){
      return user;
    };
    this.clear = function(){
      user = {};
    };
    this.init = function(data){
      if(angular.isObject(data)){
        user = data.account_info;
      }
    };
    this.query = function(id){
      var defer = $q.defer(),
        to_url = url.account +"/" + id;
      $http.get(to_url).success(function(data){
        defer.resolve(data);
      }).error(function () {
        defer.reject('UserData Query Service Error')
      });
      return defer.promise;
    };
    this.save = function(object){
      // `object` is `user` clone object
      // 成功操作之后, 更新 `user` 对象, 更新视图
      var to_url = url.account + "/" + object.id;
      if(! object.hasOwnProperty('id')){return;}
      return $http.post(to_url,object).success(function(){
        angular.extend(user,object);
        Message.show('成功修改账户信息');
      }).error(function(){
        Message.show('修改账户信息失败')
      });
    };
  }]);
