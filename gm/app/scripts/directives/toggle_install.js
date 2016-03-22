'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:toggleClass
 * @description
 * # toggleClass
 */
angular.module('mmmApp')
  .directive('toggleInstall', function () {
    return {
      restrict: 'A',
      require:'^?toggleManagement',
      link: function postLink(scope, element,attr,Ctrl) {
        Ctrl.register(element);
        element.on('click', function (event) {
          if(event.target !== element[0]){return;}
          Ctrl.toggle(element);
        });
      }
    };
  });
