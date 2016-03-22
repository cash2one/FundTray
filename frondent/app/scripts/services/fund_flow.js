'use strict';

/**
 * @ngdoc service
 * @name mmmApp.applyHelpLs
 * @description
 * # applyHelpLs
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('FundFlow',['url','$q','$http', function (url,$q,$http) {
    return {
      to:function(){
        var defer = $q.defer();
        $http.get(url.fund_flow_to)
          .success(function(data){
          defer.resolve(data);
          })
          .error(function(){defer.reject('Fund FLow TO Error')});
        return defer.promise;
      },
      from:function(){
        var defer = $q.defer();
        $http.get(url.fund_flow_from)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(){defer.reject('Fund Flow From Error')});
        return defer.promise;
      },
      sum:function(){
        var defer = $q.defer();
        $http.post(url.apply_help_list,null)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(){
            defer.resolve('Fund Flow Sum Error');
          });
        return defer.promise;
      }
    };
  }]);
