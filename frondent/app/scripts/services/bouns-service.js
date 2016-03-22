'use strict';

/**
 * @ngdoc service
 * @name mmmApp.bounsService
 * @description
 * # bounsService
 * Factory in the mmmApp.
 */
angular.module('mmmApp')
  .factory('bounsService', ['$templateRequest','$rootScope','$compile','Message',function ($templateRequest,$rootScope,$compile,Message) {
    var ele, scope = $rootScope.$new();
    $templateRequest('views/bouns.html').then(
      function(html){
        ele = $compile(html)(scope);
        scope.yes = function(){
          ele.remove(ele);
          console.log(scope.car);
          Message.show('尊敬的领导人，你的奖金还未达到购车标准，请加油！');
        }
      }
    );
    /*
    *  这里不检查DOM中是否有已经存在其他的ele,都直接插入。
    **/
    return {
      show:function(){
        angular.element(window.document.body).append(ele);
      },
      hide:function(){
        angular.element(window.document.body).remove(ele);
      }
    };
  }]);
