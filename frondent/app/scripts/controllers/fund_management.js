'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:FundManagementCtrl
 * @description
 * # FundManagementCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
  .controller('FundManagementCtrl',['$scope','Modal','Message','Upload',
    'FundService','FundFlowTo','FundFlowFrom','SystemInfo','UserData','$state','PersonInfo','expire',
    function ($scope,Modal,Message,Upload,FundService,FundFlowTo,FundFlowFrom,SystemInfo,UserData,$state,PersonInfo,expire) {
      $scope.person = PersonInfo.account_info;
      UserData.init(PersonInfo);
      // 同步个人信息；因为个人信息里面有一个重要的信息需要同步在本地
      $scope.system_info = SystemInfo;
      $scope.apply_help_ls = expire.add(FundFlowTo.apply_help_ls);

      $scope.apply_help = FundFlowTo.apply_help;
      $scope.accept_help_ls = expire.add(FundFlowFrom.apply_help_ls);

      $scope.accept_help = FundFlowFrom.accept_help;
      $scope.access_to_apply = function(){
        if($scope.apply_help.apply_order){
          Message.show('您当前已经有申请正在处理中，不可以多次重复申请');
        }else{
          $state.go('dashboard.apply_help');
        }
      };
      $scope.access_to_accept = function(){
        if($scope.apply_help.apply_order){
          Message.show('你当前还有未完成的申请帮助，请及时确认完毕，才能申请接受帮助')
        }else if($scope.accept_help.accept_order){
          Message.show('你当前已经正在接受帮助中，不可以多次重复申请')
        }else{
          $state.go('dashboard.accept_help');
        }
      };
      $scope.detail = function(object){
        Modal.open(object);
      };
      $scope.reject = function(object){
        var target = {'apply_sorder':object.apply_sorder};
        //Message.show('拒绝帮助系统将会查封您的账户，请小心注意！！');
        FundService.apply_help_refuse(target);
      };
      $scope.finish = function(object){
        Upload.open(object.apply_sorder);
      };
      $scope.confirm = function(object){
        FundService.accept_help_confirm(object);
      };
      $scope.notreceived = function(object){
        var target = {'apply_sorder':object.apply_sorder};
        FundService.accept_help_notreceived(target);
      };
      $scope.del_apply = function(object){
        var target = {'apply_order':object.apply_order};
        FundService.del_apply_help(target);
      };
      $scope.del_accept = function(object){
        var target = {'accept_order':object.accept_order};
        FundService.del_accept_help(target);
      };
      $scope.view_message = function(message){
        if(message){
          Message.show('留言为：'+message);
        }else{
          Message.show('当前没有留言');
        }
      };
    }]);
