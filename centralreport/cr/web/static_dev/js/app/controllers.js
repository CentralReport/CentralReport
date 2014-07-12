CentralReport.angularApp.controller('DashboardCtrl', function ($scope, $http, $timeout) {

    var dataGetter = function() {
        $http.get('/api/checks')
            .success(function(data) {
                $scope.checks = data;

                CentralReport.checkInterval = parseInt(data.interval, 10);
                CentralReport.initServerDelay(data.system.timestamp);

                $scope.timer = $timeout(function() { dataGetter() }, CentralReport.getNextCheckIn(data.date));
            })
            .error(function(data, status, headers, config) {
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

    dataGetter();
});

CentralReport.angularApp.controller('LeftMenuCtrl', function ($scope, $location) {
    $scope.getClass = function(path) {
        if ($location.path().substr(0, path.length) == path) {
            return "active"
        } else {
            return ""
        }
    }
});
