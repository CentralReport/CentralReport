<html>
<head>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">

    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/jquery.progressbar.js"></script>

    <title>Current Host</title>


    <script type="text/javascript">
        var progress_key = '<?= $uuid ?>';

        $(document).ready(function() {
            $("#pb1").progressBar();
            $("#pb4").progressBar(100, { showText: true, barImage: 'img/progressbg_green.gif'} );
        });

    </script>
</head>


<body>
    <div class="container">
        <div class="content">

            <div class="page-header">
                <h1>${hostname} <small>with CentralReport</small></h1>
            </div>

            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>
            <hr />

            <h3>Last check : <strong>${lastcheck}</strong></h3>
            <span class="progressBar" id="pb4"></span>

            <hr />

            Last CPU Check<br />
            User : ${cpu_user} %<br />
            System : ${cpu_system} %<br />
            Idle : ${cpu_idle} %

            <hr />

            Last Memory check :<br />
            Total : ${mem_total} MB<br />
            Free : ${mem_free} MB<br />
            Active : ${mem_active} MB<br />
            Inactive : ${mem_inactive} MB

            <hr />

            Load average : <strong>${load_1m}, ${load_5m}, ${load_15m}</strong>


        </div>
    </div>
</body>
</html>
