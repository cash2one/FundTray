'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('RegisterCtrl', ['buffer','$scope','$state','UserService','$stateParams',
    function (buffer,$scope,$state,Userserice) {
      $scope.payload = {};
      var result = /\?leader_id=(\w+)(&n)?(.*)$/.exec(window.location.href);
      if(result){
        console.log(result);
        $scope.payload.leader_id = result[1];
        $scope.payload.out_leader_id = result[1];
      }

      $scope.change_leader_id = function(){
        Userserice.leader_id().then(function(data){
          $scope.payload.leader_id = parseInt(data);
        });
      };
      $scope.person = buffer.get();
      $scope.next = function(){
        buffer.set($scope.payload);
        $state.go('register_bank');
      };
    }]);
