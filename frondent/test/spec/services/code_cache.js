'use strict';

describe('Service: codeCache', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var codeCache;
  beforeEach(inject(function (_codeCache_) {
    codeCache = _codeCache_;
  }));

  it('should do something', function () {
    expect(!!codeCache).toBe(true);
  });

});
