CentralReport.angularApp.controller('DashboardCtrl', function ($scope, $http, $timeout, $location) {

    $scope.isInitialLoad = true;

    var dataGetter = function() {
        $http.get('/api/checks')
            .success(function(data) {
                $scope.isInitialLoad = false;
                $scope.checks = data;
                $scope.error = undefined;

                // We want to refresh the interface when new data is available
                CentralReport.checkInterval = parseInt(data.interval, 10);
                CentralReport.initServerDelay(data.system.timestamp);
                $scope.timer = $timeout(function() { dataGetter() }, CentralReport.getNextCheckIn(data.date));
            })
            .error(function(data, status, headers, config) {
                $scope.error = {
                    'title': 'Unable to load data',
                    'description': 'Next try in few seconds...'
                }
                $scope.timer = $timeout(function() { dataGetter() }, 10000);
            });
    }

    var stopTimer = function() {
        if (angular.isDefined($scope.timer)) {
            $timeout.cancel($scope.timer);
            $scope.timer = undefined;
        }
    };

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        stopTimer();
    });

    $scope.getReadableByte = function(bytes) {
        return CentralReport.getReadableFileSizeString(bytes);
    }

    if ($scope.hostData === undefined) {
        $location.url('/error');
    } else {
        dataGetter();
    }
});

CentralReport.angularApp.controller('LeftMenuCtrl', function ($scope, $location) {

    $scope.isCollapsed = true;

    $scope.getClass = function(path) {
        if ($location.path().substr(0, path.length) == path) {
            return "active"
        } else {
            return ""
        }
    }
});

CentralReport.angularApp.controller('ErrorCtrl', function ($scope, $location) {
    if ($scope.error === undefined) {
        $location.url('/');
    }
});
