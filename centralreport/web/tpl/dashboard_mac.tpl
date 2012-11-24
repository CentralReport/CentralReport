<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Current Host</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/custom.css">

    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/jquery.flot.js"></script>
    <script type="text/javascript" src="js/jquery.flot.pie.js"></script>
    <script type="text/javascript" src="js/jquery.flot.selection.js"></script>

    <script type="text/javascript">

        $(document).ready(function() {

            var data = [
                { label: "User",  data: {{ cpu.user }}, hoverable: true, clickable: true},
                { label: "System",  data: {{ cpu.system }} },
                { label: "Idle",  data: {{ cpu.idle }}, color: 3}
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
                        legend: {show: false},
                        grid: {
                            hoverable: true,
                            clickable: true
                        }
                    });

            var memory_data = [
                { label: "Resident", data: {{ memory.resident }}, color: 0},
                { label: "Active",  data: {{ memory.active }}, color: 7},
                { label: "Inactive",  data: {{ memory.inactive }}, color:1},
                { label: "Free",  data: {{ memory.free }}, color: 3}

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
                <h1>{{ host.hostname }} <small>with CentralReport</small></h1>
            </div>

            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>

            <div><strong><a href="/">Back to summary</a></strong></div>

            <table class="table table-striped">
                <tbody>
                <tr>
                    <td>Kernel</td>
                    <td>{{ host.kernelName }} (Version : {{ host.kernelVersion }})</td>
                </tr>
                <tr>
                    <td>Model</td>
                    <td>{{ host.model }}</td>
                </tr>
                </tbody>
            </table>

            <hr />
            <h3>CPU</h3>
            <div class="row">
                <div class="span6">

                    <h5>Last check : {{ last_check }}</h5>
                    <p class="custom_margin_top_plus_20">Model : {{ host.cpuModel }}</p>
                    <p>Number of cores : {{ host.cpuCount }}</p>

                </div>
                <div class="span6">
                    <div id="graph_cpu" style="width:400px;height:250px"></div>
                </div>
            </div>

            <hr>

            <h3>Memory</h3>
            <div class="row">
                <div class="span6">

                    <h5>Last check : {{ last_check }}</h5>

                    <div class="custom_margin_top_plus_20">
                        <table class="table table-striped">
                            <tbody>
                            <tr>
                                <td>Total</td>
                                <td width="120px">{{ memory.total }} MB</td>
                            </tr>
                            <tr>
                                <td><strong>Free</strong></td>
                                <td><strong>{{ memory.free }} MB</strong></td>
                            </tr>
                            <tr>
                                <td>Active</td>
                                <td>{{ memory.active }} MB</td>
                            </tr>
                            <tr>
                                <td>Inactive</td>
                                <td>{{ memory.inactive }} MB</td>
                            </tr>
                            <tr>
                                <td>Residente</td>
                                <td>{{ memory.resident }} MB</td>
                            </tr>
                            </tbody>
                        </table>

                        <table class="table table-striped">
                            <tbody>
                            <tr>
                                <td>Swap</td>
                                <td width="120px">{{ memory.swapSize }} MB</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="span6">
                    <div id="graph_memory" style="width:400px;height:250px"></div>
                </div>
            </div>

            <hr>
            <h3>Load average</h3>

            <div class="row">
                <div class="span6">
                    <h5>Last check : {{ last_check }}</h5>
                    <div class="custom_margin_top_plus_20">
                        <table class="table table-striped">
                            <tbody>
                            <tr>
                                <td>Last minute</td>
                                <td>{{ loadaverage.last1m }}</td>
                            </tr>
                            <tr>
                                <td>Last 5 minutes</td>
                                <td>{{loadaverage.last5m }}</td>
                            </tr>
                            <tr>
                                <td>Last 15 minutes</td>
                                <td>{{ loadaverage.last15m }}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="span6"></div>
            </div>
            <hr>
            <h3>Disks</h3>

            <div class="row">
                <div class="span6">
                    <div class="custom_margin_top_plus_20">
                        <table class="table table-striped">
                            <thead>
                                <th>Filesystem name</th>
                                <th>Available (MB)</th>
                                <th>Used (MB)</th>
                                <th>Total (MB)</th>
                            </thead>
                            <tbody>
                                {% for disk in disks.checks %}
                                    <tr>
                                        <td>{{ disk.name }}</td>
                                        <td>{{ disk.free }}</td>
                                        <td>{{ disk.used }}</td>
                                        <td>{{ disk.size }}</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="span6"></div>
            </div>
        </div>
    </div>
</body>
</html>
