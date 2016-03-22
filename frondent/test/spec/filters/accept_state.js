'use strict';

describe('Filter: acceptState', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var acceptState;
  beforeEach(inject(function ($filter) {
    acceptState = $filter('acceptState');
  }));

  it('should return the input prefixed with "acceptState filter:"', function () {
    var text = 'angularjs';
    expect(acceptState(text)).toBe('acceptState filter: ' + text);
  });

});
