/**
 * Created by Administrator on 2016-2-22.
 */

'use strict';

angular.module('mmmApp')
  .controller('HelpCtl', ['$scope','$state', '$q','$http','url','auth','Message','AccountMgr', function ($scope,$state,$q,$http, url, auth,Message) {
    // 自动匹配
    $scope.auto_match = function () {
      var defer = $q.defer();
      var to_url = url.auto_match + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_am_apply_help_uid + '/' + $scope.to_am_accept_help_uid + '/' + $scope.to_am_apply_money
      return $http.post(to_url,null)
        .success(function(){
          Message.addCallbacks($state.go,'dashboard.auto_match');
          Message.show('自动匹配申请帮助用户:'+ $scope.to_am_apply_help_uid + '接受帮助用户:'+$scope.to_am_accept_help_uid + ',金额:'+ $scope.to_am_apply_money + '成功！');
        })
        .error(function(){
          Message.addCallbacks($state.go,'dashboard.auto_match');
          Message.show('自动匹配申请帮助用户:'+ $scope.to_am_apply_help_uid + '接受帮助用户:'+$scope.to_am_accept_help_uid + ',金额:'+ $scope.to_am_apply_money + '失败！');
        });
    };
  }]);

