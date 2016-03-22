'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:toggleClassManagement
 * @description
 * # toggleClassManagement
 */
angular.module('mmmApp')
  .directive('toggleManagement', function () {
    return {
      restrict: 'A',
      controller:function(){
        var elements = [];
        this.register = function(ele){
          elements.push(ele);
        };
        this.toggle = function(ele){
          elements.forEach(function(element){
            if(ele === element){
              element.toggleClass('active');
            }else{
              element.removeClass('active');
            }
          });
        }
      }
    };
  });
