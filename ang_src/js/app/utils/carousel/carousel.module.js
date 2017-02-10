'use strict';

angular.module('carousel', ['ui.bootstrap']);
function carousel($scope){
	$scope.myInterval = 3000;
	$scope.slides = [
	{
		"image": 'C:/Users/SHIKKAA/Desktop/LiveWithPassion/src/img/climate.jpg'
	},
	{
		"image": '/img/music.jpg'
	},	
	{
		"image": '/img/cars.jpg'
	},
	{
		"image": '/img/books.jpg'
	}
	];
}