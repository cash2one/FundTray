'use strict';

describe('Service: registerCache', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var registerCache;
  beforeEach(inject(function (_registerCache_) {
    registerCache = _registerCache_;
  }));

  it('should do something', function () {
    expect(!!registerCache).toBe(true);
  });

});
