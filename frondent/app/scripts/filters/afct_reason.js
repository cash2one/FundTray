'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:afctReason
 * @function
 * @description
 * # afctReason
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('afctReason', function () {
      var afct_reason_ls = {
          10:'下级提供帮助',
          20:'下级拒绝帮助'
      };
      return function (input) {
          return afct_reason_ls[input] ?  afct_reason_ls[input]: '系统奖励'
      };
  });
