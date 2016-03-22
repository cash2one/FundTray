'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:equalTo
 * @description
 * # equalTo
 */
angular.module('mmmApp')
    .directive('equalTo', function () {
        return {
            restrict: 'A',
            require:'?ngModel',
            scope:{
                target:'=equalTo'
            },
            link: function postLink(scope, element, attrs, ngModel) {
                if(!ngModel){ return; }
                ngModel.$validators.equality = function(modelValue,viewValue){
                    var value = modelValue || viewValue;
                    return scope.target === value;
                };
                element.on('blur',(function(){ngModel.$validate();}));
            }
        };
    });

