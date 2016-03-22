'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:afctType
 * @function
 * @description
 * # afctType
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('afctType', function () {
    return function (input) {
      return input >= 20 ? '惩罚' : '奖励'
    };
  });
