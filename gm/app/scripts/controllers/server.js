/**
 * Created by Administrator on 2016-2-22.
 */
'use strict';

angular.module('mmmApp')
  .controller('ServerCtrl', ['$scope','$state', '$q','$http','$log','url','auth','Message',
    function ($scope,$state,$q,$http,$log, url, auth,Message) {

      // 设置系统公告
      $scope.set_notice = function () {
        var defer = $q.defer();
        var to_url = url.set_notice + '/' + auth.id + '/' + auth.passwd + '/' + $scope.to_notice
        return $http.post(to_url,null)
          .success(function(data){
            Message.addCallbacks($state.go,'dashboard.set_notice');
            Message.show('设置系统公告成功！');
          })
          .error(function(){
            Message.addCallbacks($state.go,'dashboard.set_notice');
            Message.show('设置系统公告失败！');
          });
      };
    }]);

angular.module('mmmApp')
  .controller('AllServerSettingCtrl', ['$scope','$state', '$q','$http','$log','url','auth','Message','AllServerSetting',
    function ($scope,$state,$q,$http,$log, url, auth,Message,AllServerSetting) {
      $scope.AllServerSetting = AllServerSetting;
      $scope.AllServerSetting.cfmd_reward_dic = JSON.stringify(AllServerSetting.cfmd_reward_dic)
      $scope.AllServerSetting.pay_reward_dic = JSON.stringify(AllServerSetting.pay_reward_dic)

      // 重置所有系统参数
      $scope.reset_server_setting =function(ServerSettingData) {
        var to_url = url.reset_server_setting;
        return $http.post(to_url, ServerSettingData).success(function () {
          Message.addCallbacks($state.go,'dashboard.server_setting');
          Message.show('设置系统参数成功！');
        }).error(function () {
          Message.addCallbacks($state.go,'dashboard.server_setting');
          Message.show('设置系统参数失败！');
        });
      };
    }]);
