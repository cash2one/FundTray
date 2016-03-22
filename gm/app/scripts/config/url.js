'use strict';

/**
 * @ngdoc service
 * @name mmmApp.base
 * @description
 * # base
 * Value in the mmmApp.
 */
angular.module('mmmApp')
  .value('protocol','http')
  .value('domain','10.24.6.170')
  .value('port','10000')
  .factory('url',['domain','protocol','port',function(domain,protocol,port){
    var base = protocol+"://"+domain+":"+port;
    var normal = protocol+"://"+domain;
    return {
      login:base+'/gm_login',
      account:base+'/account',
      apply_help_list:base+'/apply_help_list',
      accept_help_list:base+'/accept_help_list',
      get_history_notice:base+'/get_history_notice',
      view_account:base+'/view_account',
      active_account:base+'/active_account',
      seal_account:base+'/seal_account',
      unseal_account:base+'/unseal_account',
      add_active_coin:base+'/add_active_coin',
      add_match_coin:base+'/add_match_coin',
      auto_match:base+'/auto_match',
      set_notice:base+'/set_notice',
      all_server_setting:base+'/all_server_setting',
      reset_server_setting:base+'/reset_server_setting'
    };
  }]);

