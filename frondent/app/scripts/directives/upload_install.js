'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:uploadInstall
 * @description
 * # uploadInstall
 */
angular.module('mmmApp')
  .directive('uploadInstall', ['Upload','FileSender',function (Upload,FileSender) {
    var style = {
      position:'absolute',
      top:'50%',
      left:'50%',
      transform:'translate(-50%,-50%)'
    };
    return {
      templateUrl: 'views/install/upload_install.html',
      restrict: 'E',
      replace:'true',
      scope:{},
      controller:function($scope,$element){
        $scope.reset = function(){
          var form,raw_form,img;
          form = $element.find('form');
          raw_form = form[0];
          raw_form.reset();
          img = $element.find('img');
          img.remove();
          $scope.data = {};
        };
        $scope.yes = function (){
          $element.removeClass('in');
          FileSender.add($scope.data);
          FileSender.send();
          $scope.reset();
        };
        $scope.no = function(){
          $element.removeClass('in');
          $scope.reset();
        }
      },
      link: function postLink(scope, element) {
        scope.data = {file:'',pay_msg:''};
        var input,img,raw_ele,raw_input;
        input = element.find('input');
        if(input.length!=1){return;}
        raw_input=input[0];
        input.on('change',function(){
          if(typeof FileReader === 'undefined'){
            console.log('Your browser version is too low, please use the latest version of the modern browser')
          }
          var file = raw_input.files[0];
          if(/image\/\w+/.test(file.type)){
          //if(/image\/\w+/.test(file.type) && file.size <1024*30){
            scope.data.file = file;
            scope.$digest();
            var reader = new FileReader();
            reader.onload = function(){
              img = new Image();
              img.src = this.result;
              img.style.width = "60%";
              input.after(img);
            };
            reader.readAsDataURL(file)
          }
          //else if(file.size > 1024*30){
          //  console.log('图片大小必须小于30K');
          //}
          else{}
        });
        scope.data = {};
        raw_ele = element[0];
        element.addClass('in');
        angular.extend(raw_ele.style,style);
        scope.$watch(function(){
          return Upload.timestamp
        },function(){
          FileSender.load({apply_sorder:Upload.apply_sorder});
          element.toggleClass('in')
        })
      }
    };
  }]);
