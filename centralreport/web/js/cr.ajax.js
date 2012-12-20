/**
 * CentralReport ajax functions
 *
 * DON'T USE IN PRODUCTION ENVIRONMENT - Indev version
 *
 * User: Charles-Emmanuel
 * Date: 13/12/12
 */

// Client timestamp
var actual_client_timestamp = 0;

// Last check timestamp (server side)
var last_timestamp = 0;

// Next check will be occur at this timestamp (client side)
var next_check_at = 0;

/**
 * Refresh the next check counter
 */
function updateNextCheckCounter(){

    actual_client_timestamp = Math.round(new Date().getTime() / 1000);

    if(next_check_at != 0){
        var nextCheckIn = parseInt(next_check_at - actual_client_timestamp) + parseInt(3);

        if(nextCheckIn < -5) {
            $("#ajax_enabled").html("Error. Next try in few seconds");
        }
        else if(nextCheckIn <= 0) {
            $("#ajax_enabled").html("Next check is very close !");
        } else {
            $("#ajax_enabled").html("Next check in "+ nextCheckIn +" seconds");
        }
    }

    setTimeout(updateNextCheckCounter,1000);

}


/**
 * Verify if a new check is avaiable
 */
function verifyIsNewCheckIsAvailable() {

    console.log("CR - Verify if a new check is available...");
    actual_client_timestamp = Math.round(new Date().getTime() / 1000);

    $("#ajax_enabled").html("No new check");
    $("#div_ajax_error_alert").css("display","none");

    $.ajax('/api_date_check')
        .done(function(data) {

            // If last_timestamp=0, CR hasn't done any checks yet...
            if(data["last_timestamp"] == 0) {
                $("#last_check_date").html("No check available");
                last_timestamp = 0;
            } else {
                $("#last_check_date").html(data["last_fulldate"]);

                // Now, we can getting all checks values...
                if(parseInt(data['last_timestamp']) != last_timestamp) {

                    console.log("CR - /!\\ Last timestamp has changed!");

                    $("#ajax_enabled").html("Getting last check...");

                    last_timestamp = parseInt(data['last_timestamp']);
                    server_timestamp = parseInt(data['current_timestamp']);

                    // Differences between computer clock and client clock
                    actual_client_timestamp = Math.round(new Date().getTime() / 1000)
                    diff_timestamp_client_server = server_timestamp - actual_client_timestamp;

                    // All checks are done every 60 seconds by the agent
                    next_check_at = last_timestamp + 60 + diff_timestamp_client_server;

                    updateLastCheck();

                }
            }

            // We add 4 seconds between two checks, to be sure the next check is done
            next_check_in = parseInt(next_check_at - actual_client_timestamp) + parseInt(4)
            console.log("CR - Next checks estimated in "+ next_check_in +" seconds")

            // Execute next test in 20 seconds
            if(next_check_at == 0) {
                console.log("CR - Testing if new checks are available in 20 seconds...");
                setTimeout(verifyIsNewCheckIsAvailable,20000);
            } else if(next_check_in<(-10)) {
                console.log("CR - New checks are very late... Next try in 10 seconds");
                setTimeout(verifyIsNewCheckIsAvailable,10000);
            } else if(next_check_in<(-1)) {
                console.log("CR - New checks should have been done... Do a another try in 2 seconds");
                setTimeout(verifyIsNewCheckIsAvailable,2000);
            } else if(next_check_in<3) {
                console.log("CR - Next checks are very close. Next try in 1 second");
                setTimeout(verifyIsNewCheckIsAvailable,1000);
            } else {
                console.log("CR - Testing if new checks are available in "+ next_check_in +" second(s)");
                setTimeout(verifyIsNewCheckIsAvailable,parseInt(next_check_in*1000));
            }
        })
        .fail(function() {

            $("#div_ajax_error_alert").html("Ajax error. Next try in 30 seconds...");
            $("#div_ajax_error_alert").css("display","block");
            setTimeout(verifyIsNewCheckIsAvailable,30000);

        });


}


/**
 * This function get the last check and update view values
 */
function updateLastCheck() {

    console.log("CR - Getting last check values...");

    $.getJSON('/api_full_check',function(data) {

        // Refresh last check date
        $("#last_check_date").html(data["last_fulldate"]);
        $("#last_check_date").fadeOut(300).fadeIn(300);

        // CPU
        if(data["cpu_check_enabled"] == "True") {
            $("#span_cpu_percent_value").html(data["cpu_percent"]);
            $("#span_cpu_user_value").html(data["cpu_user"]);
            $("#span_cpu_system_value").html(data["cpu_system"]);

            // Progress bar
            $("#bar_cpu_percent").css("width",data["cpu_percent"] + "%")

            // Progress bar color and status image
            var newCpuClass = "dashboard-box-status";
            var newCpuProgressBarClass = "progress progress-striped "

            switch (data["cpu_state"]) {
                case 'ok':
                    newCpuClass = "dashboard-box-status-ok";
                    newCpuProgressBarClass += "progress-success"
                    break;
                case 'warning':
                    newCpuClass = "dashboard-box-status-warning";
                    newCpuProgressBarClass += "progress-warning"
                    break;
                case 'alert':
                    newCpuClass = "dashboard-box-status-alert";
                    newCpuProgressBarClass += "progress-danger"
                    break;
            }
            $("#div_cpu_status").removeClass().addClass(newCpuClass);
            $("#div_cpu_progress").removeClass().addClass(newCpuProgressBarClass);


            $("#div_cpu_box").fadeOut(300).fadeIn(300);
        }


        // Memory and Swap
        if(data["memory_check_enabled"] == "True") {
            // Memory
            $("#span_memory_percent_value").html(data["memory_percent"]);
            $("#span_memory_free_value").html(data["memory_free"]);
            $("#span_memory_used_value").html(data["memory_used"]);

            $("#bar_memory_percent").css("width",data["memory_percent"] + "%");

            // Progress bar color and status image
            var newMemoryClass = "dashboard-box-status";
            var newCpuProgressBarClass = "progress progress-striped "

            switch (data["memory_state"]) {
                case "ok":
                    newMemoryClass = "dashboard-box-status-ok";
                    newCpuProgressBarClass += "progress-success"
                    break;
                case "warning":
                    newMemoryClass = "dashboard-box-status-warning";
                    newCpuProgressBarClass += "progress-warning"
                    break;
                case "alert":
                    newMemoryClass = "dashboard-box-status-alert";
                    newCpuProgressBarClass += "progress-danger"
                    break;
            }
            $("#div_memory_status").removeClass().addClass(newMemoryClass);
            $("#div_memory_progress").removeClass().addClass(newCpuProgressBarClass);

            $("#div_memory_box").fadeOut(300).fadeIn(300);


            // Swap
            $("#span_swap_used_value").html(data["swap_used"]);
            $("#span_swap_percent_value").html(data["swap_percent"]);

            $("#div_swap_box").fadeOut(300).fadeIn(300);
        }


        // Load average and uptime
        if(data["load_check_enabled"] == "True") {
            // Load average
            $("#span_load_percent_value").html(data["load_percent"]);
            $("#span_load_value").html(data["load_last_one"]);

            $("#bar_memory_percent").css("width",data["memory_percent"] + "%");

            // Progress bar color and status image
            var newLoadClass = "dashboard-box-status";
            var newLoadProgressBarClass = "progress progress-striped "

            switch (data["memory_state"]) {
                case "ok":
                    newLoadClass = "dashboard-box-status-ok";
                    newLoadProgressBarClass += "progress-success"
                    break;
                case "warning":
                    newLoadClass = "dashboard-box-status-warning";
                    newLoadProgressBarClass += "progress-warning"
                    break;
                case "alert":
                    newLoadClass = "dashboard-box-status-alert";
                    newLoadProgressBarClass += "progress-danger"
                    break;
            }
            $("#div_load_status").removeClass().addClass(newLoadClass);
            $("#div_load_progress").removeClass().addClass(newLoadProgressBarClass);

            $("#bar_load_percent").css("width",data["load_percent"] + "%");
            $("#div_load_box").fadeOut(300).fadeIn(300);

            // Uptime
            $("#span_uptime_full_text").html(data["uptime_full_text"]);
            $("#span_uptime_seconds_values").html(data["uptime_seconds_values"]);
            $("#span_uptime_start_date_value").html(data["start_date"]);

            $("#div_uptime_box").fadeOut(300).fadeIn(300);
        }


        $.get('/api_disks_check', function(data) {

            $("#div_disks_box").html(data);
            $("#div_disks_box").fadeOut(300).fadeIn(300);

        });

        // Reload is done!
        $("#ajax_enabled").html("Ajax reload : Done");
    });

}


$(document).ready(function() {

    // Enable Ajax auto refresh
    $("#ajax_enabled").html("Ajax refresh enabled...");

    // Enable auto-refresh next check counter
    updateNextCheckCounter();

    // Verify if a new check is available on the server
    verifyIsNewCheckIsAvailable();

});

