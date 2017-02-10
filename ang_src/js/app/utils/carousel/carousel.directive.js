'use strict';

angular.module("carousel").
	directive('carousel', function(Post, $location){
		return{
			restrict: "E",
			templateUrl: "/templates/carousel.html",
			link: function(data){
			// scope.items = Post.query()
			//  scope.selectItem = function($item, $model, $label){
			// // 	 	console.log($item)
			// // 	 	console.log($model)
			// // 	 	console.log($label)
			// 	 	$location.path("/blog/" + $item.id)
		}
	}
});