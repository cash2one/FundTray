'use strict';

describe('Service: applyStateLs', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var applyStateLs;
  beforeEach(inject(function (_applyStateLs_) {
    applyStateLs = _applyStateLs_;
  }));

  it('should do something', function () {
    expect(!!applyStateLs).toBe(true);
  });

});
