{% extends "layout/page.layout.tpl" %}

{% block title %}CentralReport dashboard{% endblock %}

{% block header_title %}CentralReport host dashboard{% endblock %}
{% block header_subtitle %}{{ hostname }}{% endblock %}

{% block content %}

            <div class="alert">
                <strong>Indev Version</strong><br />
                This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
            </div>

            <div class="headhand">
                Last check : {{ last_check }}
            </div>

            <div class="row custom_margin_top_plus_20">
                <div class="span4">

                    <div class="dashboard-box">

                        <div class="dashboard-box-headhand">
                            <div class="dashboard-box-status">

                            </div>
                            <div class="dashboard-box-title">
                                CPU
                            </div>
                        </div>

                        <div class="dashboard-box-datas">
                            <div class="title">
                                {{ cpu_percent }} %
                            </div>

                            <div class="progress progress-striped progress-success">
                                <div class="bar" style="width:{{ cpu_percent }}%;"></div>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="span4">
                    <div class="dashboard-box">
                        <div class="dashboard-box-headhand">
                            <div class="dashboard-box-status">

                            </div>
                            <div class="dashboard-box-title">
                                Memory
                            </div>
                        </div>
                        <div class="dashboard-box-datas">
                            <div class="title">
                                {{ memory_percent }} %
                            </div>

                            <div class="progress progress-striped progress-success">
                                <div class="bar" style="width:{{ memory_percent }}%;"></div>
                            </div>
                        </div>
                    </div>
                </div>


                <div class="span4">
                    <div class="dashboard-box">
                        <div class="dashboard-box-headhand">
                            <div class="dashboard-box-status">

                            </div>
                            <div class="dashboard-box-title">
                                Load Average
                            </div>
                        </div>
                        <div class="dashboard-box-datas">
                            <div class="title">
                                {{ loadaverage }}
                            </div>
                            <div class="subtitle">
                                {{ loadaverage_percent }} % of 4 cores
                            </div>

                            <div class="progress progress-striped progress-success">
                                <div class="bar" style="width:{{ loadaverage_percent }}%;"></div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div class="row">
                <div class="span12">
                    <div class="dashboard-box">
                        <div class="dashboard-box-headhand">
                        <div class="dashboard-box-status">

                        </div>
                        <div class="dashboard-box-title">
                            Uptime
                        </div>
                            </div>
                        <div class="dashboard-box-text">
                            <div class="title">
                                {{ uptime }} <small>({{ uptime_seconds }} seconds)</small>
                            </div>
                            <div class="subtitle">
                                Boot date : {{ start_date }}
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div class="row">
                <div class="span12">
                    <div class="dashboard-box">
                        <div class="dashboard-box-headhand">
                            <div class="dashboard-box-status">

                            </div>
                            <div class="dashboard-box-title">
                                Disks
                            </div>
                        </div>
                        <div class="dashboard-box-text">
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
                </div>

            </div>

            <div class="headhand headhand-center">
                <a href="dashboard">Go to old full report</a>
            </div>



{% endblock %}

{% block footer_version %}CentralReport Unix/Linux - Indev version{% endblock %}
