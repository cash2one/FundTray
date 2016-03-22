'use strict';

describe('Service: noticeService', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var noticeService;
  beforeEach(inject(function (_noticeService_) {
    noticeService = _noticeService_;
  }));

  it('should do something', function () {
    expect(!!noticeService).toBe(true);
  });

});
