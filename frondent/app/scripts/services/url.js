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
  .value('domain','52.77.234.86')
  .value('port','10000')
  .factory('url',['domain','protocol','port',function(domain,protocol,port){
    var base = protocol+"://"+domain+":"+port;
    var normal = protocol+"://"+domain;
    return {
      login:base+'/login',
      register:base+'/register',
      account:base+'/account',
      active:base+'/active',
      summary:base+'/summary',
      passwd_change:base+'/passwd_change',
      upload:normal+'/apply_help_pay',
      fund_flow_to:base+'/cur_apply_help',
      fund_flow_from:base+'/cur_accept_help',
      apply_help:base+'/apply_help',
      accept_help:base+'/accept_help',
      apply_help_refuse:base+'/apply_help_refuse',
      apply_help_list:base+'/apply_help_list',
      accept_help_confirm:base+'/accept_help_confirm',
      random_id:base+'/new_account_id',
      random_leader_id:base+'/random_leader_id',
      system_info:base+'/system_info',
      del_apply_help:base+'/del_apply_help',
      del_accept_help:base+'/del_accept_help',
      accept_help_notreceived:base+'/accept_help_notreceived',
      check_id:base+'/check_id',
      bonus_logs:base+'/get_bonus_logs',
      check_phone:base+'/check_phone',
      active_coin_transfer:base+'/active_coin_transfer',
      match_coin_transfer:base+'/match_coin_transfer'
    };
  }]);

