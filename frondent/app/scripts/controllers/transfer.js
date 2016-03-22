'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:TransferCtrl
 * @description
 * # TransferCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('TransferCtrl', ['$scope','UserService','UserData',function ($scope,UserService,UserData) {
    $scope.active_coin_transfer =function(object){
      UserService.active_coin_transfer(object)
    };
    $scope.macth_coin_transfer = function(object){
      UserService.match_coin_transfer(object)
    };
    $scope.active_coin = UserData.get().active_coin;
    $scope.match_coin = UserData.get().match_coin;
  }]);
