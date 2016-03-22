'use strict';

/**
 * @ngdoc service
 * @name mmmApp.UserService
 * @description
 * # UserService
 * Service in the mmmApp.
 */
angular.module('mmmApp')
  .service('UserService', ['$http','auth','$log','$q','url','UserData','Message','$state',
    function ($http,auth,$log,$q,url,UserData,Message,$state) {
      this.login = function(object){
        var that = this;
        return $http.post(url.login,object)
          .success(function(data){
            console.log(data);
            auth.init(data);
            data.account_info && UserData.init(data);
          })
          .error(function(data,status){
            if(status == 447 ){
              that.logout();
              $state.go('login');
              Message.show('账号已经被封号，请联系管理员.');
            }else if(status == 448){
              Message.show('账号未激活，请联系领导人.');
            }else{
              Message.show('帐号密码错误！');
            }
            $log.error('UserService Login Service Failure. status code:'+status);
          })
      };
      this.register = function(object){
        return $http.post(url.register,object)
          .success(function(data){
            return $q.resolve(data)
          })
          .error(function(data,status){
            $log.error('UserService Register Service Failure. status code:'+status);
          })
      };
      this.logout = function(){
        auth.clear();
        UserData.clear();
      };
      this.check_id = function(id){
        var data = {id:id};
        return $http.post(url.check_id,data)
      };
      this.random_id = function(){
        var defer = $q.defer();
        $http.get(url.random_id)
          .success(function(data){
            defer.resolve(data.new_account_id)
          })
          .error(function(){
            defer.reject('Time Out')
          });
        return defer.promise;
      };
      this.leader_id = function(){
        var defer = $q.defer();
        $http.get(url.random_leader_id)
          .success(function(data){
            defer.resolve(data.leader_id)
          })
          .error(function(){
            defer.rejected('Time Out')
          });
        return defer.promise;
      };
      this.active = function(object){
        var to_url = url.active+'/'+object.id;
        return $http.post(to_url,null)
          .success(function(){
            Message.show('成功激活ID为' + object.id + '的用户');
            $log.info('UserService Account Service success in active account'+object.id);
          })
          .error(function(){
            Message.show('激活失败');
            $log.info('UserService Account Service fail to active account'+object.id);
          });
      };
      this.password = function(object){
        var that = this;
        return $http.post(url.passwd_change,object)
          .success(function(){
            $log.info('UserService Password Service success in password change');
            Message.addCallbacks($state.go,'login');
            Message.addCallbacks(that.logout);
            Message.show('修改密码成功，请重新登录。');
          })
          .error(function () {
            $log.info('UserService Password Service fail to password change');
            Message.show('修改密码失败，请确认后再尝试。');
          });
      };
      this.summary = function(){
        var defer = $q.defer();
        $http.get(url.summary)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('UserService Summary Service fail to get summary');
            defer.reject(data);
          });
        return defer.promise;
      };
      this.getBonusLog = function(pageIndex){
        var defer = $q.defer();
        $http.post(url.bonus_logs,{page_idx:pageIndex})
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('UserService Bonus Log Service fail to get Bonus Log');
            defer.reject(data);
          });
        return defer.promise;
      };
      this.check_phone =  function(phone){
        var defer = $q.defer();
        $http.post(url.check_phone,phone)
          .success(function(data){
            defer.resolve(data);
          })
          .error(function(data){
            $log.info('UserService Check Phone Service fail to check phone');
            defer.reject(data);
          });
        return defer.promise;
      };
      this.active_coin_transfer = function(object){
        console.log('active done');
        $http.post(url.active_coin_transfer,object).then(
          function resolve(){
            Message.show('激活币转账成功');
            $state.go('dashboard.fund_management');
          },function reject(response){
            switch (response.status){
              case 441:
                Message.show('激活币转账失败，目标用户不存在');
                break;
              case 440:
                Message.show('激活币转账失败，请联系管理员');
                break;
              default:
                $log.info('激活币转账失败，未知错误码')
            }
          }
        )
      };
      this.match_coin_transfer = function(object){
        console.log('match done');
        $http.post(url.match_coin_transfer,object).then(
          function resolve() {
            Message.show('配单币转账成功');
            $state.go('dashboard.fund_management');
          },function reject(response){
            switch (response.status){
            case 441:
              Message.show('配单币转账失败，目标用户不存在');
              break;
            case 440:
              Message.show('配单币转账失败，请联系管理员');
              break;
            default:
              $log.info('配单币转账失败，未知错误码')
            }
          })
      }
    }]);
