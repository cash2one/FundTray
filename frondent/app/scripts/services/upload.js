'use strict';

/**
 * @ngdoc service
 * @name mmmApp.upload
 * @description
 * # upload
 * Service in the mmmApp.
 */
angular.module('mmmApp')
    .service('Upload', function () {
      // AngularJS will instantiate a singleton by calling "new" on this function
      this.timestamp = + new Date();
      this.object = {};
      this.apply_sorder = '';
      this.open = function(apply_sorder){
        console.log(apply_sorder);
        this.apply_sorder = apply_sorder;
        this.timestamp = + new Date();
      }
    });