'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:checkId
 * @description
 * # checkId
 */
angular.module('mmmApp')
  .directive('idNoExisted', ['$http','url',function ($http,url) {
    return {
      restrict: 'A',
      require:'?ngModel',
      link: function postLink(scope, element, attrs, ngModel) {
        if(!ngModel){return;}
        ngModel.$setValidity('id',false);
        element.on('blur',function(event){
            var value = ngModel.$viewValue||ngModel.$modelValue;
            if(!value){
                angular.element(event.target).next().html('');
                ngModel.$setValidity('id',false);
                return
            }
            $http.post(url.check_id,{id:value}).then(function(){
                angular.element(event.target).next().html('<i class="fa fa-lg fa-close text-danger"></i>&nbsp;账户已被注册');
                ngModel.$setValidity('id',false);
            },function(){
                angular.element(event.target).next().html('<i class="fa fa-lg fa-check text-success"></i>&nbsp;账户可以使用');
                ngModel.$setValidity('id',true);
            })
        });
      }
    };
  }]);
