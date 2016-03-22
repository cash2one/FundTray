'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:acceptState
 * @function
 * @description
 * # acceptState
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('accept_state', function () {
  var accept_state_ls ={
      0:'匹配',
      1:'完成',
      10:'匹配',
      11:'匹配'
  };
    return function (input) {
      return accept_state_ls[input] ? accept_state_ls[input]:'未知状态'
    };
  });
