/**
 * Created by Administrator on 2016-2-22.
 */

'use strict';

angular.module('mmmApp')
  .controller('AccountCtl', ['$scope','$state', '$q','$http','url','auth','Message','AccountMgr', function ($scope,$state,$q,$http, url, auth,Message, AccountMgr) {
    $scope.AccountMgr = AccountMgr;

    // 查看账户
    $scope.view_account = function () {
        var defer = $q.defer();
        var to_url = url.view_account + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_view_account
        return $http.post(to_url,null)
          .success(function(data){
            AccountMgr.init(data)
            $state.go('dashboard.show_account');
          })
          .error(function(data){});
    };

    // 激活账户
    $scope.active_account = function () {
      var defer = $q.defer();
      var to_url = url.active_account + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_active_account
      return $http.post(to_url,null)
        .success(function(){
          Message.addCallbacks($state.go,'dashboard.active_account');
          Message.show('激活账户:' + $scope.to_active_account + '成功！');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.active_account');
          Message.show('激活账户:' + $scope.to_active_account + '失败！');
        });
    };

    // 封账户
    $scope.seal_account = function () {
      var defer = $q.defer();
      var to_url = url.seal_account + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_seal_account
      return $http.post(to_url,null)
        .success(function(){
          Message.addCallbacks($state.go,'dashboard.seal_account');
          Message.show('封账户:' + $scope.to_seal_account + '成功！');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.seal_account');
          Message.show('封账户:' + $scope.to_seal_account + '失败！');
        });
    };

    // 解封账户
    $scope.unseal_account = function () {
      var defer = $q.defer();
      var to_url = url.unseal_account + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_unseal_account
      return $http.post(to_url,null)
        .success(function(){
          Message.addCallbacks($state.go,'dashboard.unseal_account');
          Message.show('解封账户:' + $scope.to_unseal_account + '成功！');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.unseal_account');
          Message.show('解封账户:' + $scope.to_unseal_account + '失败！');
        });
    };

    // 增加激活币
    $scope.add_active_coin = function () {
      var defer = $q.defer();
      var to_url = url.add_active_coin + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_add_active_account + '/' + $scope.to_add_active_coin
      return $http.post(to_url,null)
        .success(function(data){
          AccountMgr.init(data)
          $state.go('dashboard.show_account');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.add_active_coin');
          Message.show('为账户:' + $scope.to_add_active_account + '添加激活币失败！');
        });
    };
    // 增加排单币
    $scope.add_match_coin = function () {
      var defer = $q.defer();
      var to_url = url.add_match_coin + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_add_match_account + '/' + $scope.to_add_match_coin
      return $http.post(to_url,null)
        .success(function(data){
          AccountMgr.init(data)
          $state.go('dashboard.show_account');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.add_match_coin');
          Message.show('为账户:' + $scope.to_add_match_account + '添加排单币失败！');
        });
    };
  }]);
