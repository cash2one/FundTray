'use strict';

describe('Service: bounsService', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var bounsService;
  beforeEach(inject(function (_bounsService_) {
    bounsService = _bounsService_;
  }));

  it('should do something', function () {
    expect(!!bounsService).toBe(true);
  });

});
