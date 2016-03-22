'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:idExisted
 * @description
 * # idExisted
 */
angular.module('mmmApp')
  .directive('idExisted', ['$http','url','$q',function ($http,url,$q) {
      return {
          restrict: 'A',
          require:'?ngModel',
          link: function postLink(scope, element, attrs, ngModel) {
              if(!ngModel){return;}
              //ngModel.$setValidity('id',false);
              ngModel.$asyncValidators.id = function(){
                  var data={'id':ngModel.$viewValue||ngModel.$viewValue};
                  return $http.post(url.check_id,data).then(function(){
                      element.next().html('<i class="fa fa-lg fa-check text-success"></i>&nbsp;账户存在');
                      return $q.resolve('exists');
                  },function(){
                      element.next().html('<i class="fa fa-lg fa-close text-danger"></i>&nbsp;账户不存在');
                      return $q.reject('not exists');
                  })
              };
          }
      };
  }]);
