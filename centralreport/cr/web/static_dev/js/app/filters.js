CentralReport.angularApp.filter('readableBytes', function() {
    return function(rawBytes) {
        return isNaN(parseInt(rawBytes, 10)) ? '-' : CentralReport.getReadableFileSizeString(rawBytes);
    };
});

CentralReport.angularApp.filter('addNumbers', function() {
    return function(numbers) {
        var result = 0;

        for (index = 0; index < numbers.length; ++index) {
            number = parseInt(numbers[index], 10);

            if (isNaN(number)) {
                return 0;
            }

            result += number;
        }

        return result;
    };
});

CentralReport.angularApp.filter('percentage', function() {
    return function(numbers) {
        var total = parseInt(numbers['total'], 10);
        if (isNaN(total)) {
            return 0;
        }

        var sum = 0;
        for (index = 0; index < numbers['values'].length; ++index) {
            number = parseInt(numbers['values'][index], 10);

            if (isNaN(number)) {
                return 0;
            }

            sum += number;
        }

        return Math.round(sum * 100 / total, 2);
    };
});
