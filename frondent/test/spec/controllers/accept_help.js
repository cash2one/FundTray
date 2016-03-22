'use strict';

describe('Controller: AcceptHelpCtrl', function () {

  // load the controller's module
  beforeEach(module('mmmApp'));

  var AcceptHelpCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AcceptHelpCtrl = $controller('AcceptHelpCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AcceptHelpCtrl.awesomeThings.length).toBe(3);
  });
});
