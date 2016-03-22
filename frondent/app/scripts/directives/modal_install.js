'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:modalInstall
 * @description
 * # modalInstall
 */
angular.module('mmmApp')
  .directive('modalInstall', ['Modal',function (Modal) {
    var style = {
      position:'absolute',
      width:'100%',
      height:'100%'
      //top:'50%',
      //left:'50%',
      //transform:'translate(-50%,-50%)'
    };
    return {
      templateUrl: 'views/install/modal_install.html',
      restrict: 'E',
      replace:'true',
      scope:{},
      controller:function($scope,$element){
        $scope.yes = function(){
          $element.toggleClass('in');
        };
      },
      link: function postLink(scope, element) {
        var original_ele = element[0];
        element.addClass('in');
        // 因为link函数第一次就会运行一遍watch函数;添加addClass in 用来抵消
        angular.extend(original_ele.style,style);
        scope.$watch(function(){
          return Modal.timestamp;
        },function(){
          scope.item = Modal.object;
          element.toggleClass('in');
        });
      }
    };
  }]);
