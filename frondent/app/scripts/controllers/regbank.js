'use strict';

/**
 * @ngdoc function
 * @name mmmApp.controller:RegbankCtrl
 * @description
 * # RegbankCtrl
 * Controller of the mmmApp
 */
angular.module('mmmApp')
    .controller('RegbankCtrl', ['$scope','UserService','Message','buffer','$state',function ($scope,UserService,Message,buffer,$state) {
        $scope.submit = function(){
            buffer.set($scope.payload);
            UserService.register(buffer.get()).success(function(){
                var message;
                message = '注册成功，使用会员ID登录';
                buffer.clear();
                Message.addCallbacks($state.go,'login');
                Message.show(message);
            });
        };
    }]);
