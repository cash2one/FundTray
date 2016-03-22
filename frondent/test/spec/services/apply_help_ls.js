'use strict';

describe('Service: applyHelpLs', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var applyHelpLs;
  beforeEach(inject(function (_applyHelpLs_) {
    applyHelpLs = _applyHelpLs_;
  }));

  it('should do something', function () {
    expect(!!applyHelpLs).toBe(true);
  });

});
