/**
 * Created by Administrator on 2016-2-22.
 */
'use strict';

angular.module('mmmApp')
  .controller('ApplyHelpCtrl', ['$scope','$state', '$q','$http','$log','url','auth','ApplyHelpList',
    function ($scope,$state,$q,$http,$log, url, auth,ApplyHelpList) {
      $scope.apply_help_list = ApplyHelpList.apply_help_list;
  }]);

angular.module('mmmApp')
  .controller('AcceptHelpCtrl', ['$scope','$state', '$q','$http','$log','url','auth','AcceptHelpList',
    function ($scope,$state,$q,$http,$log, url, auth,AcceptHelpList) {
      $scope.accept_help_list = AcceptHelpList.accept_help_list;
    }]);

angular.module('mmmApp')
  .controller('HistoryNoticeCtrl', ['$scope','$state', '$q','$http','$log','url','auth','HistoryNotices',
    function ($scope,$state,$q,$http,$log, url, auth,HistoryNotices) {
      $scope.HistoryNotices = HistoryNotices;
    }]);


