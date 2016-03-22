'use strict';

/**
 * @ngdoc service
 * @name mmmApp.Statistics
 * @description
 * # Statistics
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('Statistics', ['$http','auth','$log','$q','url','UserData','Message','$state',
    function ($http,auth,$log,$q,url,UserData,Message,$state) {
      this.apply_help_list = function(){
        var defer = $q.defer();
        $http.post(url.apply_help_list)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('Statistics Apply Help Service fail!!!');
            defer.reject(data);
          });
        return defer.promise;
      };
      this.accept_help_list = function(){
        var defer = $q.defer();
        $http.post(url.accept_help_list)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('Statistics Accept Help Service fail!!!');
            defer.reject(data);
          });
        return defer.promise;
      };
      this.get_history_notice = function(){
        var defer = $q.defer();
        var to_url = url.get_history_notice + '/' + auth.id + '/' + auth.passwd;
        $http.post(to_url,null)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('Statistics get_history_notice Service fail!!!');
            defer.reject(data);
          });
        return defer.promise;
      };
    }]);
