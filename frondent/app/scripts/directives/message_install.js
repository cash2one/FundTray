'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:notice
 * @description
 * # body-level directive function
 */
angular.module('mmmApp')
  .directive('messageInstall', ['Message',function (Message) {
    return {
      scope:{},
      replace:'true',
      templateUrl: 'views/install/message_install.html',
      restrict: 'E',
      controller:function($scope,$element){
        $scope.yes = function (){
          $element.addClass('hide');
          Message.involveCallbacks();
        };
        $scope.no = function(){
          $element.addClass('hide');
          Message.clearCallbacks();
        };
      },
      link: function postLink(scope, element) {
        scope.$watch(
          function(){return Message.content;},
          function(n_value){
            scope.content = n_value.replace(/\d+:/,'');
            scope.level= Message.level;
            scope.content ? element.removeClass('hide') : element.addClass('hide');
          });
      }
    };
  }]);
