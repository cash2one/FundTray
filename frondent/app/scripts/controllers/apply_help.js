'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:ApplyHelpCtrl
 * @description
 * # ApplyHelpCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('ApplyHelpCtrl',['$scope','FundService','$state','UserData',function ($scope,FundService,$state,UserData) {
      $scope.minPlay = UserData.get().max_apply_money;
      $scope.apply_help = function(object){
      FundService.apply_help(object).success(function(){
        $state.go('dashboard.fund_management');
      });
    };
  }]);
