'use strict';

describe('Filter: state', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var state;
  beforeEach(inject(function ($filter) {
    state = $filter('state');
  }));

  it('should return the input prefixed with "state filter:"', function () {
    var text = 'angularjs';
    expect(state(text)).toBe('state filter: ' + text);
  });

});
