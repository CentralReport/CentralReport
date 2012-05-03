<html>
<head>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">
    <title>Current Host</title>
</head>


<body>
    <div class="container">
        <div class="content">
            <h1>CentralReport</h1>
            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>
            <hr />

            The system

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
