'use strict';

describe('Directive: modalInstall', function () {

  // load the directive's module
  beforeEach(module('mmmApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<modal-install></modal-install>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the modalInstall directive');
  }));
});
