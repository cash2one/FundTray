'use strict';

describe('Controller: SummaryCtrl', function () {

  // load the controller's module
  beforeEach(module('mmmApp'));

  var SummaryCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SummaryCtrl = $controller('SummaryCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(SummaryCtrl.awesomeThings.length).toBe(3);
  });
});
