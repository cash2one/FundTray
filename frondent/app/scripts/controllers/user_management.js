'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:UserManagementCtrl
 * @description
 * # UserManagementCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('UserManagementCtrl',['$scope','UserService','UserData',function ($scope,UserService,UserData) {
    $scope.auth = UserData.get();
    $scope.password = function (object) {
      UserService.password(object);
    };
    $scope.active = function(object){
      UserService.active(object);
    };
    $scope.account = function(object){
      var user = angular.copy(UserData.get());
      angular.extend(user,object);
      UserData.save(user).success(function(){
       // 清除视图，但是 `硬编码`, 内伤
       $scope.payload = {};
      });
    };
  }]);
