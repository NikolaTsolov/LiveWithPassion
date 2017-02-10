'use strict';

angular.module('post').
	factory('Post', function($resource){
		var url = '/api/posts/:id'
		return $resource(url, {}, {
			querry: {
				method: "GET",
				params: {},
				isArray: true,
				cache: false,
				// transformResponse
				// interceptor
			},
			get: {
				method: "GET",
				params: {id: "@id"},
				isArray: true,
				cache: false,

			}
		})
	});