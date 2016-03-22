'use strict';

describe('Service: noticeCache', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var noticeCache;
  beforeEach(inject(function (_noticeCache_) {
    noticeCache = _noticeCache_;
  }));

  it('should do something', function () {
    expect(!!noticeCache).toBe(true);
  });

});
