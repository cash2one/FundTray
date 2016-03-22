'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:SummaryCtrl
 * @description
 * # SummaryCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('SummaryCtrl', ['$scope','summary',function ($scope,summary) {
    $scope.summarys = summary.summary;
  }]);
