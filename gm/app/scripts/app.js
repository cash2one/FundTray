'use strict';

/**
 * @ngdoc overview
 * @name mmmApp
 * @description
 * # mmmApp
 *
 * Main module of the application.
 */
angular
  .module('mmmApp', [
    'ngResource',
    'ui.router',
    'ngMessages'
  ])
  .config(function ($stateProvider,$urlRouterProvider,role) {
    $urlRouterProvider.otherwise('/login');
    $stateProvider
      .state('login',{
        url:'/login',
        controller:'LoginCtrl',
        templateUrl:'views/gm_account/login.html'
      })
      .state('dashboard',{
        url:'/dashboard',
        abstract:true,
        access_level:role.user,
        views:{
          '':{
            templateUrl:'views/dashboard/dashboard.html',
            controller:'DashboardCtrl'
          },
          'header@dashboard':{
            templateUrl:'views/dashboard/header.html',
            controller:'DashboardCtrl'
          },
          'list@dashboard':{
            templateUrl:'views/dashboard/list.html',
            controller:'DashboardCtrl'
          },
          'detail@dashboard':{
            templateUrl:'views/dashboard/main_board.html',
            controller:'DashboardCtrl'
          }
        }
      })
      .state('dashboard.main_board',{
        url:'/main_board',
        access_level:role.user,
        resolve: {
        }
      })
      .state('dashboard.apply_help_list',{
        url:'/apply_help_list',
        access_level:role.user,
        resolve: {
          ApplyHelpList: function (Statistics) {
            return Statistics.apply_help_list();
          }
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/statistics/apply_help_list.html',
            controller:'ApplyHelpCtrl'
          }
        }
      })
      .state('dashboard.accept_help_list',{
        url:'/accept_help_list',
        access_level:role.user,
        resolve: {
          AcceptHelpList: function (Statistics) {
            return Statistics.accept_help_list();
          }
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/statistics/accept_help_list.html',
            controller:'AcceptHelpCtrl'
          }
        }
      })
      .state('dashboard.get_history_notice',{
        url:'/get_history_notice',
        access_level:role.user,
        resolve: {
          HistoryNotices: function (Statistics) {
            return Statistics.get_history_notice();
          }
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/statistics/history_notice_list.html',
            controller:'HistoryNoticeCtrl'
          }
        }
      })
      .state('dashboard.view_account',{
        url:'/view_account',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/view_account.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.show_account', {
        url: '/show_account',
        access_level: role.user,
        views: {
          'detail@dashboard': {
            templateUrl: 'views/account/show_account.html',
            controller: 'AccountCtl'
          }
        }
      })
      .state('dashboard.active_account',{
        url:'/active_account',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/active_account.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.seal_account',{
        url:'/seal_account',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/seal_account.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.unseal_account',{
        url:'/unseal_account',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/unseal_account.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.add_active_coin',{
        url:'/add_active_coin',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/add_active_coin.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.add_match_coin',{
        url:'/add_match_coin',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/account/add_match_coin.html',
            controller:'AccountCtl'
          }
        }
      })
      .state('dashboard.auto_match',{
        url:'/auto_match',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/help/auto_match.html',
            controller:'HelpCtl'
          }
        }
      })
      .state('dashboard.set_notice',{
        url:'/set_notice',
        access_level:role.user,
        resolve: {
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/server/set_notice.html',
            controller:'ServerCtrl'
          }
        }
      })
      .state('dashboard.server_setting',{
        url:'/server_setting',
        access_level:role.user,
        resolve: {
          AllServerSetting: function (ServerService) {
            return ServerService.all_server_setting();
          }
        },
        views:{
          'detail@dashboard':{
            templateUrl:'views/server/server.html',
            controller:'AllServerSettingCtrl'
          }
        }
      })
});
