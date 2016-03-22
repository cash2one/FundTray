'use strict';

describe('Filter: jobLevel', function () {

  // load the filter's module
  beforeEach(module('mmmApp'));

  // initialize a new instance of the filter before each test
  var jobLevel;
  beforeEach(inject(function ($filter) {
    jobLevel = $filter('jobLevel');
  }));

  it('should return the input prefixed with "jobLevel filter:"', function () {
    var text = 'angularjs';
    expect(jobLevel(text)).toBe('jobLevel filter: ' + text);
  });

});
