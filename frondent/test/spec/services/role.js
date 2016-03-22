'use strict';

describe('Service: role', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var role;
  beforeEach(inject(function (_role_) {
    role = _role_;
  }));

  it('should do something', function () {
    expect(!!role).toBe(true);
  });

});
