'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:checkPhone
 * @description
 * # checkPhone
 */
angular.module('mmmApp')
  .directive('checkPhone',['$http','$q','url', function ($http,$q,url) {
    return {
        restrict: 'A',
        require:'?ngModel',
        link: function postLink(scope, element, attrs, ngModel) {
            if(!ngModel){return;}
            //ngModel.$setValidity('id',false);
            ngModel.$asyncValidators.phone = function(){
                var data = {'phone':ngModel.$viewValue||ngModel.$modelValue};
                return $http.post(url.check_phone,data)
                    .success(function(){
                        element.next().html('<i class="fa fa-lg fa-check text-success"></i>&nbsp;手机号可以使用');
                        return $q.resolve('exists');
                    })
                    .error(function(){
                        element.next().html('<i class="fa fa-lg fa-close text-danger"></i>&nbsp;手机号已经被注册');
                        return $q.reject('not exists');
                    });
            };
        }
    };
  }]);
