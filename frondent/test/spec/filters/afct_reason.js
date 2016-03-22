'use strict';

describe('Filter: afctReason', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var afctReason;
  beforeEach(inject(function ($filter) {
    afctReason = $filter('afctReason');
  }));

  it('should return the input prefixed with "afctReason filter:"', function () {
    var text = 'angularjs';
    expect(afctReason(text)).toBe('afctReason filter: ' + text);
  });

});
