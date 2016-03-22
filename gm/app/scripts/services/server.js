'use strict';
/**
 * Created by Administrator on 2016-2-22.
 */

angular.module('mmmApp')
  .service('ServerService', ['$http','auth','$log','$q','url',
    function ($http,auth,$log,$q,url) {
      this.all_server_setting = function () {
        var defer = $q.defer();
        var to_url = url.all_server_setting
        $http.post(to_url,null)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            defer.reject(data);
          });
        return defer.promise;
      };
    }]);
