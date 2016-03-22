'use strict';

describe('Filter: afctType', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var afctType;
  beforeEach(inject(function ($filter) {
    afctType = $filter('afctType');
  }));

  it('should return the input prefixed with "afctType filter:"', function () {
    var text = 'angularjs';
    expect(afctType(text)).toBe('afctType filter: ' + text);
  });

});
