'use strict';

describe('Controller: BonusLogCtrl', function () {

  // load the controller's module
  beforeEach(module('mmmApp'));

  var BonusLogCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    BonusLogCtrl = $controller('BonusLogCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(BonusLogCtrl.awesomeThings.length).toBe(3);
  });
});
