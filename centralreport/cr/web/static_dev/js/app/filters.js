CentralReport.angularApp.filter('readableBytes', function() {
    return function(rawBytes) {
        return isNaN(parseInt(rawBytes, 10)) ? '-' : CentralReport.getReadableFileSizeString(rawBytes);
    };
});

CentralReport.angularApp.filter('readableUptime', function() {
    return function(seconds) {

        seconds = parseInt(seconds);
        if (isNaN(seconds)) {
            return '-';
        }

        var ONE_SECOND = 1;
        var ONE_MINUTE = 60;
        var ONE_HOUR = 60 * 60;
        var ONE_DAY = 60 * 60 * 24;
        var ONE_YEAR = 60 * 60 * 24 * 365;

        var remaining_seconds = seconds;
        var result_string = '';

        if (remaining_seconds >= ONE_YEAR) {
            var years = remaining_seconds / ONE_YEAR;
            years = Math.floor(years);

            remaining_seconds -= years * ONE_YEAR;

            result_string = years == 1 ? '1 year ' : years + ' years ';
        }

        if (remaining_seconds >= ONE_DAY) {
            var days = remaining_seconds / ONE_DAY;
            days = Math.floor(days);

            remaining_seconds -= days * ONE_DAY;
            result_string += days == 1 ? '1 day ' : days + ' days ';
        }

        if (remaining_seconds >= ONE_HOUR) {
            var hours = remaining_seconds / ONE_HOUR;
            hours = Math.floor(hours);

            remaining_seconds -= hours * ONE_HOUR;
            result_string += hours == 1 ? '1 hour ' : hours + ' hours ';
        }

        if (remaining_seconds >= ONE_MINUTE) {
            var minutes = remaining_seconds / ONE_MINUTE;
            minutes = Math.floor(minutes);

            remaining_seconds -= minutes * ONE_MINUTE;
            result_string += minutes == 1 ? '1 minute ' : minutes + ' minutes ';
        }

        if (remaining_seconds >= ONE_SECOND) {
            result_string += remaining_seconds == 1 ? '1 second' : remaining_seconds + ' seconds';
        }

        return result_string;
    };
});
