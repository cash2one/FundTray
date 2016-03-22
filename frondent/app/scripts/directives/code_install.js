'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:canvas
 * @description
 * # canvas
 */
angular.module('mmmApp')
  .directive('codeInstall', ['codeCache',function (codeCache) {
      var setting = {
          'font':"bold 34px Arial",
          'textBaseline':'top'
      };
      // delete q,y,p,g,j due to  q,y,p,g,j is so ugly .
      // delete 0 and O due to 0 is look like o .
      // delete lower case
      var collection = '' +
          //'wertuioasdfhklzxcvbnm' +
          'QWERTYUIPASDFGHJKLZXCVBNM' +
          '123456789' +
          '123456789' +
          '123456789' ;
          //'123456789' +
          //'123456789';
    return {
      scope:{
          width:'@',
          height:'@'
      },
      template: '<canvas></canvas>',
      restrict: 'E',
      replace:true,
      link: function postLink(scope, element, attrs) {
          var canvas = element[0],some_string;
          canvas.width = scope.width||136;
          canvas.height = scope.height||34;
          var context = canvas.getContext('2d');
          angular.extend(context,setting);
          some_string = random_string(4);
          codeCache.set(some_string);
          context.fillText(some_string,0,0);

          element.on('click',function(){
              var some_string;
              context.clearRect(0,0,canvas.width,canvas.width);
              some_string = random_string(4);
              codeCache.set(some_string);
              context.fillText(some_string,0,0);
          });
      }
    };
    function random_choice(str){
      if(typeof str =='string'){
        return str[parseInt(Math.random()*str.length)];
      }
    }
    function random_string(len){
      var result = [];
      for(var i=0;i<len;i++){
        result.push(random_choice(collection));
      }
      return result.join('');
    }
  }]);
