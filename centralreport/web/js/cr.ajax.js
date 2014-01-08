/**
 * CentralReport ajax functions
 *
 * DON'T USE IN PRODUCTION ENVIRONMENT - Indev version
 *
 * User: Charles-Emmanuel
 * Date: 13/12/12
 */

var actualClientTimestamp = 0;  // Client timestamp
var lastTimestamp = 0;  // Last check timestamp (server side)
var nextCheckAt = 0;  // Next check will be occur at this timestamp (client side)
var checksInterval = 60; // Interval between two checks

var CHECKS_INTERVAL_DEFAULT = 60; // Default interval between two checks

/**
 * Refresh the next check counter
 */
var updateNextCheckCounter = function () {
    var nextCheckIn = 0;
    var ajaxEnabledElement;
    var actualClientTimestamp;
    var ajaxEnabledElementText = '';

    if (0 !== nextCheckAt){
        actualClientTimestamp = Math.round(new Date().getTime() / 1000);
        nextCheckIn = parseInt(nextCheckAt - actualClientTimestamp, 10) + 3;

        ajaxEnabledElement = $('#ajax_enabled');

        if (nextCheckIn < -5) {
            ajaxEnabledElementText = 'Error. Next try in few seconds';
        } else if (nextCheckIn <= 0) {
            ajaxEnabledElementText = 'Next check is very close!';
        } else {
            ajaxEnabledElementText = 'Next check in ' + nextCheckIn + ' seconds';
        }

        ajaxEnabledElement.text(ajaxEnabledElementText);
    }

    setTimeout(updateNextCheckCounter, 1000);
};


/**
 * Verifies if a new check is available
 */
var verifyIsNewCheckIsAvailable = function () {
    var ajaxEnabledElement = $('#ajax_enabled');
    var ajaxErrorAlertElement = $('#div_ajax_error_alert');
    var logText = '';

    console.log('CR - Verify if a new check is available...');
    actualClientTimestamp = Math.round(new Date().getTime() / 1000);

    ajaxEnabledElement.text('No new check');
    ajaxErrorAlertElement.hide();

    $.ajax('/api/check/date')
        .done(function(data) {

            // Getting interval between two checks
            checksInterval = isNaN(data["checks_interval"]) ? CHECKS_INTERVAL_DEFAULT: parseInt(data["checks_interval"], 10);

            // If lastTimestamp=0, CR hasn't done any checks yet...
            if (0 === data['last_timestamp']) {
                $('#last_check_date').text('No check available');
                lastTimestamp = 0;
            } else {
                $('#last_check_date').text(data['last_fulldate']);

                // Now, we can getting all checks values...
                if (parseInt(data['last_timestamp'], 10) !== lastTimestamp) {

                    console.log('CR - /!\\ Last timestamp has changed!');

                    ajaxEnabledElement.text('Getting last check...');

                    lastTimestamp = parseInt(data['last_timestamp'], 10);
                    server_timestamp = parseInt(data['current_timestamp'], 10);

                    // Differences between computer clock and client clock
                    actualClientTimestamp = Math.round(new Date().getTime() / 1000);

                    if (server_timestamp < actualClientTimestamp){
                        diff_timestamp_client_server = actualClientTimestamp - server_timestamp;
                    } else {
                        diff_timestamp_client_server = server_timestamp - actualClientTimestamp;
                    }

                    // All checks are done every 60 seconds by the agent
                    nextCheckAt = lastTimestamp + checksInterval + diff_timestamp_client_server;

                    updateLastCheck();
                }
            }

            // We add 4 seconds between two checks, to be sure the next check is done
            var nextCheckIn = parseInt(nextCheckAt - actualClientTimestamp, 10) + parseInt(4, 10);
            console.log('CR - Next checks estimated in ' + nextCheckIn + ' seconds');

            // Execute next test in 20 seconds
            if (0 === nextCheckAt) {
                logText = 'Testing if new checks are available in 20 seconds...';
                time = 20000;
            } else if (nextCheckIn < -10) {
                logText = 'New checks are very late... Next try in 10 seconds';
                time = 10000;
            } else if (nextCheckIn < -1) {
                logText = 'New checks should have been done... Do a another try in 2 seconds';
                time = 2000;
            } else if (nextCheckIn < 3) {
                logText = 'Next checks are very close. Next try in 1 second';
                time = 1000;
            } else {
                logText = 'Testing if new checks are available in ' + nextCheckIn + ' second(s)';
                time = parseInt(nextCheckIn * 1000, 10);
            }

            console.log('CR - ' + logText);
            setTimeout(verifyIsNewCheckIsAvailable, time);
        })
        .fail(function() {
            ajaxErrorAlertElement.text('Ajax error. Next try in 30 seconds...');
            ajaxErrorAlertElement.show();

            setTimeout(verifyIsNewCheckIsAvailable, 30000);
        });
};


/**
 * This function get the last check and update view values
 */
var updateLastCheck = function () {
    var lastCheckDate = $('#last_check_date');
    var dataCpuPercent;
    var dataMemoryPercent;
    var newMemoryClass = 'dashboard-box-status';
    var newSwapClass = 'dashboard-box-status';
    var newCpuProgressBarClass = 'progress progress-striped ';
    var newMemoryProgressBarClass = 'progress progress-striped ';
    var newSwapProgressBarClass = 'progress progress-striped ';
    var newLoadProgressBarClass = 'progress progress-striped ';

    console.log('CR - Getting last check values...');

    $.getJSON('/api/check/full', function(data) {

        dataCpuPercent = data['cpu_percent'];
        dataMemoryPercent = data['memory_percent'];
        newMemoryClass = 'dashboard-box-status';
        // Refresh last check date

        lastCheckDate.text(data['last_fulldate']);
        lastCheckDate.fadeOut(300).fadeIn(300);

        // CPU
        if (data['cpu_check_enabled'] === 'True') {
            $('#span_cpu_percent_value').text(dataCpuPercent);
            $('#span_cpu_user_value').text(data['cpu_user']);
            $('#span_cpu_system_value').text(data['cpu_system']);

            // Progress bar
            createProgressBar('#bar_cpu_percent', dataCpuPercent);

            switch (data['cpu_state']) {
                case 'ok':
                    newCpuClass = 'dashboard-box-status-ok';
                    newCpuProgressBarClass += 'progress-success';
                    break;
                case 'warning':
                    newCpuClass = 'dashboard-box-status-warning';
                    newCpuProgressBarClass += 'progress-warning';
                    break;
                case 'alert':
                    newCpuClass = 'dashboard-box-status-alert';
                    newCpuProgressBarClass += 'progress-danger';
                    break;
            }
            $('#div_cpu_status').removeClass().addClass(newCpuClass);
            $('#div_cpu_progress').removeClass().addClass(newCpuProgressBarClass);


            $('#div_cpu_box').fadeOut(300).fadeIn(300);
        }


        // Memory and Swap
        if ('True' === data['memory_check_enabled']) {
            // Memory
            $('#span_memory_percent_value').text(dataMemoryPercent);
            $('#span_memory_free_value').text(data['memory_free']);
            $('#span_memory_used_value').text(data['memory_used']);

            createProgressBar('#bar_memory_percent', dataMemoryPercent);

            switch (data['memory_state']) {
                case 'ok':
                    newMemoryClass = 'dashboard-box-status-ok';
                    newMemoryProgressBarClass += 'progress-success';
                    break;
                case 'warning':
                    newMemoryClass = 'dashboard-box-status-warning';
                    newMemoryProgressBarClass += 'progress-warning';
                    break;
                case 'alert':
                    newMemoryClass = 'dashboard-box-status-alert';
                    newMemoryProgressBarClass += 'progress-danger';
                    break;
            }
            $('#div_memory_status').removeClass().addClass(newMemoryClass);
            $('#div_memory_progress').removeClass().addClass(newMemoryProgressBarClass);

            $('#div_memory_box').fadeOut(300).fadeIn(300);

            // Swap
            switch (data['swap_configuration']) {
                case 'unlimited':
                    $("#span_swap_used_value").text(data['swap_used']);
                    $("#span_swap_percent_value").text(data['swap_percent']);

                    switch (data['swap_state']) {
                        case 'ok':
                            newSwapClass = 'dashboard-box-status-ok';
                            break;
                        case 'warning':
                            newSwapClass = 'dashboard-box-status-warning';
                            break;
                        case 'alert':
                            newSwapClass = 'dashboard-box-status-alert';
                            break;
                    }
                    $('#div_swap_status').removeClass().addClass(newSwapClass);

                    break;
                case 'limited':
                    $("#span_swap_used_value").text(data['swap_used']);
                    $("#span_swap_size_value").text(data['swap_total']);
                    $("#span_swap_percent_value").text(data['swap_percent']);

                    // Refresh progress bar
                    createProgressBar('#bar_swap_percent', data['swap_percent']);

                    switch (data['swap_state']) {
                        case 'ok':
                            newSwapClass = 'dashboard-box-status-ok';
                            newSwapProgressBarClass += 'progress-success';
                            break;
                        case 'warning':
                            newSwapClass = 'dashboard-box-status-warning';
                            newSwapProgressBarClass += 'progress-warning';
                            break;
                        case 'alert':
                            newSwapClass = 'dashboard-box-status-alert';
                            newSwapProgressBarClass += 'progress-danger';
                            break;
                    }
                    $('#div_swap_status').removeClass().addClass(newSwapClass);
                    $('#div_swap_progress').removeClass().addClass(newSwapProgressBarClass);

                    break;

            }

            $('#span_swap_used_value').text(data['swap_used']);
            $('#span_swap_percent_value').text(data['swap_percent']);

            $('#div_swap_box').fadeOut(300).fadeIn(300);
        }


        // Load average and uptime
        if (data['load_check_enabled'] === 'True') {
            // Load average
            $('#span_load_percent_value').text(data['load_percent']);
            $('#span_load_value').text(data['load_last_one']);

            createProgressBar('#bar_load_percent', data['load_percent']);

            switch (data['load_state']) {
                case 'ok':
                    newLoadClass = 'dashboard-box-status-ok';
                    newLoadProgressBarClass += 'progress-success';
                    break;
                case 'warning':
                    newLoadClass = 'dashboard-box-status-warning';
                    newLoadProgressBarClass += 'progress-warning';
                    break;
                case 'alert':
                    newLoadClass = 'dashboard-box-status-alert';
                    newLoadProgressBarClass += 'progress-danger';
                    break;
            }
            $('#div_load_status').removeClass().addClass(newLoadClass);
            $('#div_load_progress').removeClass().addClass(newLoadProgressBarClass);


            $('#div_load_box').fadeOut(300).fadeIn(300);

            // Uptime
            $('#span_uptime_full_text').text(data['uptime_full_text']);
            $('#span_uptime_seconds_value').text(data['uptime_seconds']);
            $('#span_uptime_start_date_value').text(data['start_date']);
            $('#div_uptime_box').fadeOut(300).fadeIn(300);
        }

        $.get('/api/check/disks', function(data) {
            var disksBoxElement = $('#div_disks_box');
            disksBoxElement.html(data);
            disksBoxElement.fadeOut(300).fadeIn(300);

        });

        $('#ajax_enabled').text('Ajax reload: Done');
    });
};


/*
 * Set the width of a progress bar
 */
var createProgressBar = function (element, value) {
    $(element).css('width', value + '%');
};


/*
 * Initialization
 */
$(function () {
    $('#ajax_enabled').text('Ajax refresh enabled...');  // Enable Ajax auto refresh
    updateNextCheckCounter();
    verifyIsNewCheckIsAvailable();
});
