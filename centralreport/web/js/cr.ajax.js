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
 * Verify if a new check is avaiable
 */
function testNewCheck() {

    console.log("CR - Verify if a new check is available...");
    actual_client_timestamp = Math.round(new Date().getTime() / 1000)

    $("#ajax_enabled").html("No new check");

    $.getJSON('/api_date_check',function(data) {

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

        // 2 seconds to be sure to
        next_check_in = parseInt(next_check_at - actual_client_timestamp) + parseInt(4)
        console.log("CR - Next checks estimated in "+ next_check_in +" seconds")

        // Execute next test in 20 seconds
        if(next_check_at == 0) {
            console.log("CR - Testing if new checks are available in 20 seconds...");
            setTimeout(testNewCheck,20000);
        } else if(next_check_in<(-10)) {
            console.log("CR - New checks are very late... Next try in 10 seconds");
            setTimeout(testNewCheck,10000);
        } else if(next_check_in<(-1)) {
            console.log("CR - New checks should have been done... Do a another try in 2 seconds");
            setTimeout(testNewCheck,2000);
        } else if(next_check_in<3) {
            console.log("CR - Next checks are very close. Next try in 1 second");
            setTimeout(testNewCheck,1000);
        } else {
            console.log("CR - Testing if new checks are available in "+ next_check_in +" second(s)");
            setTimeout(testNewCheck,parseInt(next_check_in*1000));
        }

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

            $("#bar_cpu_percent").css("width",data["cpu_percent"] + "%")
            $("#div_cpu_box").fadeOut(300).fadeIn(300);
        }

        // Memory and Swap
        if(data["memory_check_enabled"] == "True") {
            // Memory
            $("#span_memory_percent_value").html(data["memory_percent"]);
            $("#span_memory_free_value").html(data["memory_free"]);
            $("#span_memory_used_value").html(data["memory_used"]);

            $("#bar_memory_percent").css("width",data["memory_percent"] + "%");
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

    testNewCheck();

});

