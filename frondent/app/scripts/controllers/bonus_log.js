'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:BonusLogCtrl
 * @description
 * # BonusLogCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('BonusLogCtrl', ['$scope','bonusLogs','UserService','Message',function ($scope,bonusLogs,UserService,Message) {
      $scope.bonusLogs = bonusLogs.bonus_logs;
      $scope.pageIndex = 2;
      $scope.getMorebonusLog = function(){
        var promise = UserService.getBonusLog($scope.pageIndex);
          promise.then(function(response){
              if(response.bonus_logs.length==0){
                  Message.show('已经没有其他消息了！！！');
                  return
              }
              $scope.bonusLogs=$scope.bonusLogs.concat(response.bonus_logs);
              $scope.pageIndex = $scope.pageIndex+1;
          })
      }
  }]);
