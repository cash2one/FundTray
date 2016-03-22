'use strict';

describe('Directive: uploadInstall', function () {

  // load the directive's module
  beforeEach(module('mmmApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<upload-install></upload-install>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the uploadInstall directive');
  }));
});
