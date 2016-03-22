"use strict";

angular.module('mmmApp')
  .config(function($httpProvider){
    $httpProvider.interceptors.push('interceptor');
  });
