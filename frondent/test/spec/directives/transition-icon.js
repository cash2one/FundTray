'use strict';

describe('Directive: transitionIcon', function () {

  // load the directive's module
  beforeEach(module('mmmApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<transition-icon></transition-icon>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the transitionIcon directive');
  }));
});
