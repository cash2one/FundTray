'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:state
 * @function
 * @description
 * # state
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('apply_state', function () {
    var apply_state_ls ={
      0:'匹配',
      1:'完成',
      2:'订单异常',
      10:'排队',
      11:'匹配'
    };
    return function (input) {
      return apply_state_ls[input]?apply_state_ls[input]:'未知状态'
    };
  });

angular.module('mmmApp')
  .filter('apply_pay_state', function () {
    var apply_state_ls ={
      0:'等待支付',
      1:'已经支付',
      2:'确认支付',
      3:'订单异常，联系客服处理',
      4:'拒绝支付'
    };
    return function (input) {
      return apply_state_ls[input]?apply_state_ls[input]:'未知状态'
    };
  });
