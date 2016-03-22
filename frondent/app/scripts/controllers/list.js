'use strict';


angular.module('mmmApp')
  .controller('ListCtrl', ['Message','$scope','bounsService',function (Message,$scope,bounsService) {
    $scope.announcement = function(){
      //Message.show('尊敬的领导人，你的奖金还未达到购车标准，请加油！');
      bounsService.show();
    }
  }]);
