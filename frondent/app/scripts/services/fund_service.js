'use strict';

/**
 * @ngdoc service
 * @name mmmApp.fundService
 * @description
 * # fundService
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('FundService', ['$http','url','$log','$state','auth','UserData','Message',function ($http,url,$log,$state,auth,UserData,Message) {
    this.apply_help = function(object){
      return $http.post(url.apply_help,object)
        .success(function (data) {
          $log.info('apply help success return data '+ JSON.stringify(data));
        })
        .error(function(data){
          $log.info('apply help failure return data ' + JSON.stringify(data));
        })
    };
    this.accept_help = function(object){
      return $http.post(url.accept_help,object)
        .success(function(data){
          $state.go('dashboard.fund_management');
          $log.info('accept_help success return data')
        })
        .error(function(){
          $log.info('accept_help success return data')
        })
    };
    this.accept_help_confirm = function(object){
      return $http.post(url.accept_help_confirm,object)
        .success(function(){
          $state.reload();
        })
        .error(function(data){
          console.log(data);
        })
    };
    this.accept_help_notreceived = function(object){
      return $http.post(url.accept_help_notreceived,object)
        .success(function(){
          $state.reload();
        })
        .error(function(data){
          console.log(data)
        })
    };
    this.apply_help_refuse = function(object){
      var result;
      result = Message.addCallbacks($http.post,url.apply_help_refuse,object);
      result.then(function(){
        $state.go('login');
        auth.clear();
        UserData.clear()
      });
      //Message.addCallbacks($state.go,'login');
      //Message.addCallbacks(function(){auth.clear()});
      //Message.addCallbacks(function(){UserData.clear()});
      Message.show('拒接支付，将会被系统封号',1);

    };
    this.del_apply_help = function(object){
      return $http.post(url.del_apply_help,object)
        .success(function(){
          $state.reload();
        })
    };
    this.del_accept_help = function(object){
      return $http.post(url.del_accept_help,object)
        .success(function(){
          $state.reload();
        })
    }
  }]);
