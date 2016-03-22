'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:expire
 * @function
 * @description
 * # expire
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('expire', function () {
    function fix2ten(num){
        if(num<10){
            num = '0'+num;
        }
        return num
    }
    return function (input) {
      var hour,minute,second;
      if (input<=0){
          return '时效过期'
      }
      hour = fix2ten(parseInt(input/3600));
      minute = fix2ten(parseInt((input%3600)/60));
      second = fix2ten(input%60);
      return hour + '小时' + minute +'分钟' + second +'秒';
    };
  });
