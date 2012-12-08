{% extends "layout/page.layout.tpl" %}

{% block title %}CentralReport dashboard{% endblock %}

{% block header_title %}CentralReport host dashboard{% endblock %}
{% block header_subtitle %}{{ hostname }}{% endblock %}

{% block content %}

            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>

            <div class="box">
                Last check : {{ last_check }}
            </div>

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
                        <h4>{{ uptime }}</h4>
                        <h4>({{ uptime_seconds }} seconds)</h4>
                        <br />
                        <h4>Since : {{ start_date }}</h4>
                    </div>

                </div>
            </div>


            <div class="box box-center">
                <a href="dashboard">Go to full report</a>
            </div>



{% endblock %}

{% block footer_version %}CentralReport Unix/Linux - Indev version{% endblock %}
