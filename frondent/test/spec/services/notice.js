'use strict';

describe('Service: notice', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var notice;
  beforeEach(inject(function (_notice_) {
    notice = _notice_;
  }));

  it('should do something', function () {
    expect(!!notice).toBe(true);
  });

});
