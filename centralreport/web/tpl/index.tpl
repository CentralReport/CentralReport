<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>CentralReport dashboard</title>

    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/custom.css">
    <script type="text/javascript" src="js/jquery.js"></script>
</head>
<body>
    <div class="container">
        <div class="content">

            <div class="page-header">
                <h2>
                    {{ hostname }} dashboard
                    <small>by CentralReport</small>
                </h2>
            </div>

            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>

            <div>
                <strong>
                    <a href="dashboard">Go to full report</a>
                </strong>
            </div>

            <hr />

            <h4>Last check : {{ last_check }}</h4>

            <div class="row custom_margin_top_plus_20">
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>CPU</h3>
                        <h2>{{ cpu_percent }} %</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width:{{ cpu_percent }}%;"></div>
                        </div>
                    </div>
                </div>
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>Memory</h3>
                        <h2>{{ memory_percent }} %</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width:{{ memory_percent }}%;"></div>
                        </div>
                    </div>
                </div>
                <div class="span4">
                    <div class="well" style="text-align: center;">
                        <h3>Load Average</h3>
                        <h2>{{ loadaverage }}</h2>
                        <div class="progress progress-striped progress-success">
                            <div class="bar" style="width:{{ loadaverage_percent }}%;">{{ loadaverage_percent }} % of 4 cores</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="span8">
                    <div class="well" style="text-align: center;">
                        <h3>Disks</h3>
                        <table class="table table-striped">
                            <tbody>
                                {% for disk in disks %}
                                    <tr>
                                        <td width="33%"><strong>{{ disk.name }}</strong></td>
                                        <td width="33%">{{ disk.free }} MB free ({{ disk.percent }} % used)</td>
                                        <td width="33%">
                                            <div class="progress progress-striped progress-success">
                                                <div class="bar" style="width:{{ disk.percent }}%;"></div>
                                            </div>
                                        </td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>

                    </div>

                </div>
                <div class="span4">

                    <div class="well" style="text-align: center;">
                        <h3>Uptime</h3>
                        <h2>{{ uptime }} sec</h2>
                        <h4>{{ start_date }}</h4>
                    </div>

                </div>
            </div>
        </div>
    </div>
</body>
</html>
