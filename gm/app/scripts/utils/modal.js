'use strict';

/**
 * @ngdoc service
 * @name mmmApp.modal
 * @description
 * # modal
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('Modal', ['UserData',function (UserData) {
    this.timestamp = + new Date();
    this.object = {};
    this.open = function(object){
      var that = this;
      UserData.query(object.accept_uid).then(function(data){
        angular.extend(that.object,object,data.account_info);
        that.timestamp = +new Date();
      });
    };
  }]);
