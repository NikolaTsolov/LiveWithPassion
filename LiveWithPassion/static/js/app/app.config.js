'use strict';

angular.module('LiveWithPassion').
	config(
		function(
			$locationProvider,
			$routeProvider
			){
			$locationProvider.html5Mode({
				enabled:true
			})

			$routeProvider.
			when("/", {
				// templateUrl: "/templates/ang/app/blog-list.html"
				template:"<blog-list></blog-list>"
			}).
			when("/about", {
				templateUrl: "/templates/about.html"
			}).
			when("/blog", {
				template: "<blog-list></blog-list>"
				// redirectTo: '/'
			}).
			when("/carousel", {
				template: "<blog-list></blog-list>"
			}).
			when("/blog/:id", {
				template: "<blog-detail></blog-detail>"
			}).
			// when("/blog/:id/abc", {
			// 	template: "<blog-list</blog-list>"
			// }).
			// when("/blog/2", {
			// 	template:"<blog-list></blog-list>"
			// }).
			otherwise({
				template: "Not Found"
				})

	});