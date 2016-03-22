'use strict';

describe('Controller: ApplyHelpCtrl', function () {

  // load the controller's module
  beforeEach(module('mmmApp'));

  var ApplyHelpCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ApplyHelpCtrl = $controller('ApplyHelpCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ApplyHelpCtrl.awesomeThings.length).toBe(3);
  });
});
