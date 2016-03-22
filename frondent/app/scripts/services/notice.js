'use strict';

/**
 * @ngdoc service
 * @name mmmApp.notice
 * @description
 * # notice
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('notice', ['$http','url','$q',function ($http,url,$q) {
    var defer;
      defer = $q.defer();
      $http.get(url.system_info).success(function(data){defer.resolve(data.notice)});
    return defer.promise;
  }]);
