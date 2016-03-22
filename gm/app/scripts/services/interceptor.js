'use strict';

/**
 * @ngdoc service
 * @name mmmApp.interceptor
 * @description
 * # interceptor
 * Factory in the mmmApp.
 * http访问拦截器
 */
angular.module('mmmApp')
  .factory('interceptor',['auth','$rootScope','$q',function (auth,$rootScope,$q) {
    return {
      request: function (config) {
        if(auth.isLoggedin){
          config.headers = config.headers || {};
          config.headers.Authorization = auth.access_token;
          config.headers.id = auth.id;
        }
        return config;
      },
      response:function(resp){
        return resp;
      },
      responseError: function (resp) {
        switch (resp.status){
          case 442:
            $rootScope.$broadcast('442 error');
            break;
          case 443:
            $rootScope.$broadcast('443 error');
            break;
          case 444:
            $rootScope.$broadcast('444 error');
            break;
          case 447:
            $rootScope.$broadcast('447 error');
            break;
          case 448:
            $rootScope.$broadcast('448 error');
            break;
          default:
            $rootScope.$broadcast('error');
        }
        return $q.reject(resp);
      }
    };
  }]);
