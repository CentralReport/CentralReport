<html>
<head>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">

    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/jquery.progressbar.js"></script>
    <script type="text/javascript" src="js/jquery.flot.js"></script>
    <script type="text/javascript" src="js/jquery.flot.pie.js"></script>
    <script type="text/javascript" src="js/jquery.flot.selection.js"></script>

    <title>Current Host</title>


    <script type="text/javascript">
        var progress_key = '<?= $uuid ?>';

        $(document).ready(function() {
            $("#pb1").progressBar();
            $("#pb4").progressBar(100, { showText: true, barImage: 'img/progressbg_green.gif'} );


            var data = [
                { label: "User",  data: ${cpu_user}, hoverable: true, clickable: true},
                { label: "System",  data: ${cpu_system}},
                { label: "Idle",  data: ${cpu_idle}, color: 3}
            ];

            $.plot($("#graph4"), data,
                    {
                        series: {
                            pie: {
                                show: true,
                                radius: 1,
                                label: {
                                    show: true,
                                    radius: 3/4,
                                    formatter: function(label, series){
                                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
                                    },
                                    background: {
                                        opacity: 0.5,
                                        color: '#000'
                                    }
                                }
                            }
                        },
                        legend: {
                            show: false
                        },
                        grid: {
                            hoverable: true,
                            clickable: true
                        }
                    });

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
            <h3>CPU</h3>
            <div class="row">
                <div class="span6">
                    <div style="">Test</div>
                </div>
                <div class="span6">
                    <div id="graph4" style="width:400px;height:250px"></div>
               </div>
            </div>





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
