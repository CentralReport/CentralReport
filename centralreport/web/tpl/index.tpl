<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/custom.css">


    <script type="text/javascript" src="js/jquery.js"></script>


    <title>Current Host</title>

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

            <div><strong><a href="dashboard">Go to full report</a></strong></div>

            <div class="row custom_margin_top_plus_20">
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>CPU</h3>
                        <br />
                        <h2>${cpu_percent} %</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width: ${cpu_percent}%;"></div>
                        </div>
                    </div>
                </div>
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>Memory</h3>
                        <br />
                        <h2>${memory_percent} %</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width: ${memory_percent}%;"></div>
                        </div>
                    </div>
                </div>
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>Load Average</h3>
                        <br />
                        <h2>${loadaverage}</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width: ${loadaverage_percent}%;">${loadaverage_percent} % of 4 cores</div>
                        </div>
                    </div>
                </div>
            </div>


        </div>
    </div>
</body>
</html>
