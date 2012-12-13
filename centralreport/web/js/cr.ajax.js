/**
 * CentralReport ajax functions
 *
 * DON'T USE IN PRODUCTION ENVIRONMENT - Indev version
 *
 * User: Charles-Emmanuel
 * Date: 13/12/12
 */

/* Some vars... */
last_timestamp = 0

/**
 * Verify if a new check is avaiable
 */
function testNewCheck() {

    console.log("CR - Verify if a new check is available...");

    $.getJSON('/api_date_check',function(data) {

        if(data["last_timestamp"] == 0) {
            $("#last_check_date").html("No check available");
        } else {
            $("#last_check_date").html(data["last_fulldate"]);

            // Now, we can getting all checks values...
            last_timestamp = parseInt(data['last_timestamp']);
        }

    });
}

/**
 * This function get the last check and update view values
 */
function updateLastCheck() {

    console.log("CR - Getting last check values...");



}

$(document).ready(function() {

    // Enable Ajax auto refresh
    $("#ajax_enabled").html("Ajax refresh enabled !");

    testNewCheck();

});

