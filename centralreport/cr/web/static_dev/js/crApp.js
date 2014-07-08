
// Default interval between two checks, in milliseconds
var DEFAULT_INTERVAL = 10000;

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

crApp.controller('DashboardCtrl', function ($scope, $http, $interval) {

    // $interval object
    var timer;

    var dataGetter = function() {
        $http.get('/api/checks').success(function(data) {
            $scope.checks = data;
        });
    }

    var initTimer = function() {
        // Don't start a new timer if we have already one
        if ( angular.isDefined(timer) ) return;

        // Default

        timer = $interval(function() {
            dataGetter();
        }, 3000);
    };

    var stopTimer = function() {
        if (angular.isDefined(timer)) {
            $interval.cancel(timer);
            timer = undefined;
        }
    };

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        stopTimer();
    });

    dataGetter();
    initTimer();

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
