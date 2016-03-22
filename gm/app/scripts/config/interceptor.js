"use strict";

angular.module('mmmApp')
  .config(function($httpProvider){
    // 注册拦截器，封装http请求和结果处理
    $httpProvider.interceptors.push('interceptor');
  });
