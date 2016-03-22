'use strict';

/**
 * @ngdoc directive
 * @name mmmApp.directive:lock
 * @description
 * # lock
 */
angular.module('mmmApp')
  .directive('lock', ['lockCount',function (lockCount) {
    var state,checked,raw_x,d_x,offset_x;
    return {
      scope:{target:'='},
      template: '<div class="lock">' +
      '<div class="lock-body"></div>' +
      '<div class="lock-text">请按住滑块,拖动到最右边</div>'+
      '<span class="lock-header" ondragstart="return false"></span>'+
      '</div>',
      replace:true,
      restrict: 'E',
      link: function postLink(scope, element) {
        lockCount.reset();
        var count = lockCount.getCount();
        var target = lockCount.getTarget();
        scope.$watch(function(){
          return lockCount.getCount()
        },function(){
          count = lockCount.getCount();
        });
        scope.$watch(function(){
          return lockCount.getTarget()
        },function(){
          target = lockCount.getTarget();
        });
        var div = element.children()[0];
        var text = element.children()[1];
        var span = element.children()[2];
        div.style.width=0;
        span.style.left=0;
        element.on('mousedown',function(event){
          if(count == target){return}
          if(event.target === span){
            state='active';
            raw_x = event.clientX;
            offset_x = event.offsetX;
          }
        });
        element.on('mousemove',function(event){
          if(count == target){return}
          //if(checked){return;}
          if(state==='active'){
            d_x = event.clientX-raw_x;
            if(d_x<=0){return;}
            else if(d_x>=300){
              state = 'deactive';
              count = count + 1;
              //checked=true;
              text.innerText='验证通过';
              element.addClass('ready');
              scope.$parent.$apply(function(){
                scope.target=true;
              });
            }else{
              span.style.left = d_x+'px';
              div.style.width = d_x+'px';
            }
          }
        });
        element.on('mouseup',function(event){
          if(count == target){return}
          if(event.target === span){
            state = 'deactive';
            d_x = event.clientX-raw_x;
            if(d_x){
              var func = function(){
                setTimeout(function(){
                  span.style.left = d_x+'px';
                  div.style.width = d_x+'px';
                  if(d_x!==0){
                    d_x=d_x-1;
                    func();
                  }
                });
              };
              setTimeout(function(){
                func();
              },50);
            }
          }
        });
        element.on('mouseout',function(event){
          if(count == target){return}
          if(event.target === span){
            state = 'deactive';
            span.style.left = '0'+'px';
            div.style.width = 0+'px';
          }
        });
      }
    };
  }]);
