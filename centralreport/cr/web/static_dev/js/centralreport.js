
var CentralReport = {
    DEFAULT_CHECK_INTERVAL: 10,
    CHECK_DURATION: 4,
    CLIENT_TIMEZONE_OFFSET: new Date().getTimezoneOffset() * 60,

    checkInterval: 0,
    serverDelay: 0,

    angularApp: undefined,

    initServerDelay: function(serverTimestamp) {
        serverDelay = this.getUTCtimestamp() - parseInt(serverTimestamp, 10);
    },

    getNextCheckIn: function(lastCheck) {
        var checksInterval = this.checkInterval === 0 ? this.DEFAULT_CHECK_INTERVAL: parseInt(this.checkInterval, 10);
        var nextCheckAt = parseInt(lastCheck, 10) + checksInterval + this.serverDelay;

        var nextCheckIn = parseInt(nextCheckAt, 10) - this.getUTCtimestamp() + this.CHECK_DURATION;

        if (nextCheckIn <= 0) {
            return this.DEFAULT_CHECK_INTERVAL * 1000;
        }

        return nextCheckIn * 1000;
    },

    getUTCtimestamp: function() {
        return (Math.round(new Date().getTime() / 1000)) - this.CLIENT_TIMEZONE_OFFSET;
    },

    getReadableFileSizeString: function(fileSizeInBytes) {
        fileSizeInBytes = parseInt(fileSizeInBytes, 10);
        var i = 0;
        var byteUnits = [' B', ' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
        while (fileSizeInBytes > 1000){
            fileSizeInBytes = fileSizeInBytes / 1000;
            i++;
        };

        return Math.max(fileSizeInBytes, 0).toFixed(1) + byteUnits[i];
    },

    isValidJson: function(json) {
        try {
            JSON.parse(json);
            return true;
        } catch (e) {
            return false;
        }
    }
}

