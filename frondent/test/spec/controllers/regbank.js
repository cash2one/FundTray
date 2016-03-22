'use strict';

describe('Controller: RegbankCtrl', function () {

  // load the controller's module
  beforeEach(module('mmmApp'));

  var RegbankCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    RegbankCtrl = $controller('RegbankCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(RegbankCtrl.awesomeThings.length).toBe(3);
  });
});
