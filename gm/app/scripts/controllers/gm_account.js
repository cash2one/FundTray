'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('LoginCtrl', ['$http','$scope','$state','url','Message','auth','UserData',function($http, $scope,$state,url,Message,auth,UserData) {
      $scope.login = function(){
        var that = this;
        return $http.post(url.login,$scope.person)
          .success(function(data){
            auth.setpasswd($scope.person.passwd)
            auth.init(data);
            data.account_info && UserData.init(data);
            $state.go('dashboard.main_board');
          })
          .error(function(data,status){
            if(status == 447 ){
              that.logout();
              $state.go('login');
              Message.show('账号已经被封号，请联系管理员.');
            }else if(status == 448){
              Message.show('账号未激活，请联系领导人.');
            }else{
              Message.show('帐号密码错误！');
            }
            $log.error('Statistics Login Service Failure. status code:'+status);
          })
      };
      this.logout = function(){
        auth.clear();
        UserData.clear();
      };
  }]);
