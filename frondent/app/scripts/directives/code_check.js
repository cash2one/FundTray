'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:verifyCode
 * @description
 * # verifyCode
 */
angular.module('mmmApp')
    .directive('codeCheck', ['codeCache',function (codeCache) {
        return {
            restrict: 'A',
            require:'?ngModel',
            link: function postLink(scope, element, attrs, ngModel) {
                if(!ngModel){ return; }
                ngModel.$validators.correct = function(modelValue,viewValue){
                    var value = modelValue || viewValue;
                    return codeCache.verify(value);
                };
                element.on('blur',(function(){ngModel.$validate();}));
            }
        };
    }]);
