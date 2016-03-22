'use strict';

/**
 * @ngdoc service
 * @name mmmApp.auth
 * @description
 * # auth
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .service('auth', ['role',function (role) {
    // Service logic
    // 仅保存 `授权` 字段 id, access_token
    // load 服务端返回数据 account_info
    this.isLoggedin = false;
    this.role = role.pub;
    this.clear = function(){
      this.isLoggedin = false;
      this.role = role.pub;
      delete this.access_token;
      delete  this.id
    };
    this.init = function (data) {
      var account = data.account_info;
      if(!angular.isObject(account)){return;}
      this.id = account.id;
      this.access_token = data.access_token;
      this.isLoggedin = true;
      this.role = role.user;
    };
    this.isAuthorized = function(level){
      return this.role>=level;
    };
  }]);
