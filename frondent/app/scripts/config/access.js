"use strict";

angular.module('mmmApp')
  .run(['$rootScope','auth','$state','role',function($rootScope,auth,$state,role){
    $rootScope.force_reload = function(){
      if ($state.is('dashboard.fund_management')){
        $state.reload('dashboard.fund_management');
      }else{
        $state.go('dashboard.fund_management');
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
