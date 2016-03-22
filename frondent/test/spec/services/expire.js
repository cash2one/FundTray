'use strict';

describe('Service: expire', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var expire;
  beforeEach(inject(function (_expire_) {
    expire = _expire_;
  }));

  it('should do something', function () {
    expect(!!expire).toBe(true);
  });

});
