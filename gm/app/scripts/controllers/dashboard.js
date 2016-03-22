'use strict';

/**
 * @ngdoc function
 * @name mmm2App.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the mmm2App
 */
angular.module('mmmApp')
  .controller('DashboardCtrl', ['$scope','$state','Message',function ($scope,$state,Message) {
    $scope.$on('error',function(){
        if($state.is('dashboard.main_board')){
            $state.reload('dashboard.main_board');
        }else{
            $state.go('dashboard.main_board');
        }
    });

  }]);
