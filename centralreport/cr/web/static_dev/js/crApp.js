
var crApp = angular.module('crApp', ['ngRoute']);

crApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider
            .when('/dashboard', {
                templateUrl: '/static/partials/dashboard.html',
                controller: 'DashboardCtrl'
            })
            .when('/settings', {
                templateUrl: '/static/partials/settings.html'
            })
            .otherwise({
                redirectTo: '/dashboard'
            });
    }]);

crApp.controller('DashboardCtrl', function ($scope, $http) {
    $http.get('/api/checks').success(function(data) {
        $scope.checks = data;
    });

    $http.get('/api/checks').success(function(data) {
        $scope.checks = data;
    });
});

crApp.controller('LeftMenuCtrl', function ($scope, $location) {
    $scope.getClass = function(path) {
        if ($location.path().substr(0, path.length) == path) {
            return "active"
        } else {
            return ""
        }
    }
});
crApp.directive('crLeftMenu', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/partials/left_menu.html'
    };
});
