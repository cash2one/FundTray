'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:transitionIcon
 * @description
 * # transitionIcon
 */
angular.module('mmmApp')
  .directive('transitionIcon', ['$rootScope',function ($rootScope) {
    return {
      link: function postLink(scope, element) {

        element.addClass('hide');

        $rootScope.$on('$stateChangeStart',function(event,toState){
          if(toState.name === 'dashboard.main_board'){
            element.removeClass('hide');
          }
        });

        $rootScope.$on('$stateChangeSuccess',function(){
          element.addClass('hide');
        });

        $rootScope.$on('$stateChangeError',function(){
          element.addClass('hide');
        });
      }
    };
  }]);
