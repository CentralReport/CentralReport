CentralReport.angularApp = angular.module('crApp', ['ngRoute', 'ui.bootstrap']);

CentralReport.angularApp.config(
    [
        '$routeProvider',
        function($routeProvider) {
            $routeProvider
                .when('/dashboard', {
                    templateUrl: '/static/partials/dashboard.html',
                    controller: 'DashboardCtrl'
                })
                .when('/host', {
                    templateUrl: '/static/partials/host.html'
                })
                .when('/error', {
                    controller: 'ErrorCtrl',
                    templateUrl: '/static/partials/error.html'
                })
                .otherwise({
                    redirectTo: '/dashboard'
                });
        }
    ]
);

CentralReport.angularApp.run(function ($rootScope, $http, $location) {
    $http.get('/api/host')
        .success(function(data) {
            $rootScope.hostData = data;
        })
        .error(function(data, status, headers, config) {
            $rootScope.hostData = undefined;

            $rootScope.error = {
                'title': 'Oops!',
                'description': 'Cannot get host data. Next try in few seconds...'
            }
        });
});
