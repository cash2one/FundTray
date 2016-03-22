'use strict';

describe('Directive: equalTo', function () {

  // load the directive's module
  beforeEach(module('mmm2App'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<equal-to></equal-to>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the equalTo directive');
  }));
});
