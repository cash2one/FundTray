'use strict';

/**
 * @ngdoc service
 * @name mmmApp.lockCount
 * @description
 * # lockCount
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('lockCount', function () {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var count = 0;// default count is 1
    var target = 1;
    this.add = function(){
      count = count+1;
    };
    this.getCount = function(){
      return count;
    };
    this.getTarget = function(){
      return target;
    };
    this.reset = function(){
      count = 0;
      target = 1;
    }
  });
