'use strict';

/**
 * @ngdoc filter
 * @name mmmApp.filter:jobLevel
 * @function
 * @description
 * # jobLevel
 * Filter in the mmmApp.
 */
angular.module('mmmApp')
  .filter('jobLevel', function () {
    var job_level ={
      '0':'无职位',
      '1':'经理',
      '2':'副经理',
      '3':'总经理'
    };
    return function (input) {
      return job_level[input] ? job_level[input] : '未知';
    };
  });
