<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/custom.css">


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

            $.plot($("#graph_cpu"), data,
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

            var memory_data = [
                { label: "Resident", data: ${mem_resident}, color: 0},
                { label: "Active",  data: ${mem_active}, color: 7},
                { label: "Inactive",  data: ${mem_inactive}, color:1},
                { label: "Free",  data: ${mem_free}, color: 3}

            ];

            $.plot($("#graph_memory"), memory_data,
                    {
                        series: {
                            pie: {
                                show: true,
                                radius: 1,
                                label: {
                                    show: true,
                                    radius: 3/4,
                                    formatter: function(label, series){
                                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'+label+'<br/>'+ Math.round(series.percent)+'%</div>';
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

        <table class="table table-striped">
            <tbody>
            <tr>
                <td>Kernel</td>
                <td>${kernel} (Version : ${kernel_version})</td>
            </tr>
            <tr>
                <td>Model</td>
                <td>${mac_model}</td>
            </tr>
            </tbody>
        </table>

        <hr />
        <h3>CPU</h3>
        <div class="row">
            <div class="span6">

                <h5>Last check : ${cpu_date}</h5>
                <p class="custom_margin_top_plus_20">Model : ${cpu_model}</p>
                <p>Number of cores : ${ncpu}</p>

            </div>
            <div class="span6">
                <div id="graph_cpu" style="width:400px;height:250px"></div>
            </div>
        </div>





        <hr />

        <h3>Memory</h3>
        <div class="row">
            <div class="span6">

                <h5>Last check : ${mem_date}</h5>

                <div class="custom_margin_top_plus_20">
                    <table class="table table-striped">
                        <tbody>
                        <tr>
                            <td>Total</td>
                            <td width="120px">${mem_total} MB</td>
                        </tr>
                        <tr>
                            <td><strong>Free</strong></td>
                            <td><strong>${mem_free} MB</strong></td>
                        </tr>
                        <tr>
                            <td>Active</td>
                            <td>${mem_active} MB</td>
                        </tr>
                        <tr>
                            <td>Inactive</td>
                            <td>${mem_inactive} MB</td>
                        </tr>
                        <tr>
                            <td>Residente</td>
                            <td>${mem_resident} MB</td>
                        </tr>
                        </tbody>
                    </table>

                    <table class="table table-striped">
                        <tbody>
                        <tr>
                            <td>Swap</td>
                            <td width="120px">${mem_swap} MB</td>
                        </tr>
                        </tbody>
                    </table>

                </div>

            </div>
            <div class="span6">
                <div id="graph_memory" style="width:400px;height:250px"></div>
            </div>
        </div>

        <hr />
        <h3>Load average</h3>

        <div class="row">
            <div class="span6">

                <h5>Last check : ${load_date}</h5>

                <div class="custom_margin_top_plus_20">
                    <table class="table table-striped">
                        <tbody>
                        <tr>
                            <td>Last minute</td>
                            <td>${load_1m}</td>
                        </tr>
                        <tr>
                            <td>Last 5 minutes</td>
                            <td>${load_5m}</td>
                        </tr>
                        <tr>
                            <td>Last 15 minutes</td>
                            <td>${load_15m}</td>
                        </tr>
                        </tbody>
                    </table>

                </div>

            </div>
            <div class="span6">
                &nbsp;
            </div>
        </div>

        <hr />
        <h3>Disks</h3>

        <div class="row">
            <div class="span6">

                <div class="custom_margin_top_plus_20">
                    <table class="table table-striped">
                        <thead>
                        <th>Filesystem name</th>
                        <th>Available</th>
                        <th>Used</th>
                        <th>Total</th>
                        </thead>
                        <tbody>
                        % for disk in disks:
                        <tr>
                            <td>${disk['filesystem']|h}</td>
                            <td>${disk['free']|h}</td>
                            <td>${disk['used']|h}</td>
                            <td>${disk['total']|h}</td>
                        </tr>
                        % endfor
                        </tbody>
                    </table>

                </div>

            </div>
            <div class="span6">
                &nbsp;
            </div>
        </div>


    </div>
</div>
</body>
</html>
