'use strict';

describe('Service: lockCount', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var lockCount;
  beforeEach(inject(function (_lockCount_) {
    lockCount = _lockCount_;
  }));

  it('should do something', function () {
    expect(!!lockCount).toBe(true);
  });

});
