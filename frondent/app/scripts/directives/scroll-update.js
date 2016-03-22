'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:scrollUpdate
 * @description
 * # scrollUpdate
 */
angular.module('mmmApp')
  .directive('scrollUpdate', function () {
    return {
      restrict: 'A',
      scope:{callback:'&callback'},
      link: function postLink(scope, element) {
        element.on('mousewheel',function(){
          if(element[0].scrollHeight == element[0].clientHeight+element[0].scrollTop){
            scope.callback();
          }
        })
      }
    };
  });
