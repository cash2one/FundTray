'use strict';

describe('Service: fundService', function () {

  // load the service's module
  beforeEach(module('mmmApp'));

  // instantiate service
  var fundService;
  beforeEach(inject(function (_fundService_) {
    fundService = _fundService_;
  }));

  it('should do something', function () {
    expect(!!fundService).toBe(true);
  });

});
