'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:toggleClass
 * @description
 * # activeInstall
 */
angular.module('mmmApp')
  .directive('activeInstall', function () {
    return {
      restrict: 'A',
      scope:{
        flag:'=',
        target:'@'
      },
      link: function postLink(scope, element) {
        element.on('click', function () {
          //var ele = event.target;
          //console.log (scope.flag == scope.target);
          //if(event.target !== element[0] || scope.flag == scope.target){return;}
          //element.toggleClass('active')
        });
        element.on('mouseout',function(){
          if(event.target === element[0]){
            console.log('mouse out');
          }
        });
      }
    };
  });
