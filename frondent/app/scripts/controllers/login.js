'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('LoginCtrl', ['$scope','UserService','$state','Message','lockCount',function($scope,UserService,$state,Message,lockCount) {
    lockCount.reset();
    $scope.login = function () {
      UserService.login($scope.person)
        .success(function(){
          $state.go('dashboard.fund_management');
        })
        .error(function(){});
    };
  }]);
