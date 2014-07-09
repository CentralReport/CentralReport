
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

CentralReport.angularApp.run(function ($rootScope, $http) {
    $http.get('/api/host').success(function(data) {
        console.log(data);
        $rootScope.hostData = data;
    });
});
