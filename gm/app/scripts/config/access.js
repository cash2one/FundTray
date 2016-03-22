"use strict";

// 提供ctrl f5 强制刷新的处理策略

angular.module('mmmApp')
  .run(['$rootScope','auth','$state','role',function($rootScope,auth,$state,role){
    $rootScope.force_reload = function(){
      if ($state.is('dashboard.main_board')){
        $state.reload('dashboard.main_board');
      }else{
        $state.go('dashboard.main_board');
      }
    };
    $rootScope.$on('$stateChangeStart',function(event,toState){
      var level = toState.access_level||role.pub;
      if(!auth.isAuthorized(level)){
        event.preventDefault();
        $state.go('login');
      }
    });
  }]);
