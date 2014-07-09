
CentralReport.angularApp = angular.module('crApp', ['ngRoute']);

CentralReport.angularApp.config(
    [
        '$routeProvider',
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
        }
    ]
);
