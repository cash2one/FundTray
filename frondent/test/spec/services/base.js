'use strict';

describe('Service: base', function () {

  // load the service's module
  beforeEach(module('mmm2App'));

  // instantiate service
  var base;
  beforeEach(inject(function (_base_) {
    base = _base_;
  }));

  it('should do something', function () {
    expect(!!base).toBe(true);
  });

});
