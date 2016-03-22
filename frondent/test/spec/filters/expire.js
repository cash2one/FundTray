'use strict';

describe('Filter: expire', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var expire;
  beforeEach(inject(function ($filter) {
    expire = $filter('expire');
  }));

  it('should return the input prefixed with "expire filter:"', function () {
    var text = 'angularjs';
    expect(expire(text)).toBe('expire filter: ' + text);
  });

});
