'use strict';

describe('Service: urlencode', function () {

  // load the service's module
  beforeEach(module('mmm2App'));

  // instantiate service
  var urlencode;
  beforeEach(inject(function (_urlencode_) {
    urlencode = _urlencode_;
  }));

  it('should do something', function () {
    expect(!!urlencode).toBe(true);
  });

});
