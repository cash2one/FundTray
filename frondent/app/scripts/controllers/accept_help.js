'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:AcceptHelpCtrl
 * @description
 * # AcceptHelpCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('AcceptHelpCtrl', ['$scope','FundService','UserData',
    function ($scope,FundService,UserData) {
    $scope.account_info = UserData.get();
    $scope.accept_help = function(object){
      FundService.accept_help({mafuluo:object});
    };
  }]);
