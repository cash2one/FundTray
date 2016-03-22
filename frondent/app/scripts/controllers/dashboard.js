'use strict';

/**
 * @ngdoc function
 * @name mmm2App.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the mmm2App
 */
angular.module('mmmApp')
  .controller('DashboardCtrl', ['$scope','$state','Message','UserService',function ($scope,$state,Message,UserService) {
    $scope.$on('error',function(){
        if($state.is('dashboard.fund_management')){
            $state.reload('dashboard.fund_management');
        }else{
            $state.go('dashboard.fund_management');
        }
    });
    $scope.$on('442 error',function(){
        Message.show('当日资金达到上限，请改天再来申请！');
        $state.go('dashboard.fund_management');
    });
    $scope.$on('443 error',function(){
        Message.show('你的排单币不足，请联系管理员！');
        $state.go('dashboard.fund_management');
    });
    $scope.$on('444 error',function(){
       Message.show('每一次申请的金额，不得到低于上一次投资金额');
       $state.go('dashboard.fund_management');
    });
    $scope.$on('447 error',function(){
      UserService.logout();
      $state.go('login');
      Message.show('账号已经被封号，请联系管理员');
    });
    $scope.$on('448 error',function(){
      Message.show('账号未激活，请联系领导人.');
      //$state.go('dashboard.fund_management');
    })
  }]);
