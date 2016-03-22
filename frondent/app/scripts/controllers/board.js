'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:BoardCtrl
 * @description
 * # BoardCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('BoardCtrl', ['$stateParams','$scope',function ($stateParams,$scope) {
    $scope.id = $stateParams.id;
  }]);
