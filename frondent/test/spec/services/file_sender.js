'use strict';

describe('Service: fileSender', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var fileSender;
  beforeEach(inject(function (_fileSender_) {
    fileSender = _fileSender_;
  }));

  it('should do something', function () {
    expect(!!fileSender).toBe(true);
  });

});
