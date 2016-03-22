'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:marqueenInstall
 * @description
 * # marqueenInstall
 */
angular.module('mmmApp')
  .directive('marqueenInstall', ['notice',function (notice) {
    var template="<marquee><p>" +
        "<i class='fa fa-star'></i>" + "{{notice}}" +
        "</p></marquee>";
    return {
      scope:{},
      template: template,
      restrict: 'E',
      replace:true,
      link: function postLink(scope, element) {
          notice.then(function(data){scope.notice = data;});
          element.on('mouseover',function(){
              element[0].stop();
          });
          element.on('mouseout',function(){
             element[0].start();
          });
      }
    };
  }]);
