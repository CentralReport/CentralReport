{% extends "layout/page.layout.tpl" %}

{% block title %}{{ hostname }} dashboard - CentralReport{% endblock %}

{% block header_title %}CentralReport host dashboard{% endblock %}
{% block header_subtitle %}{% endblock %}

{% block content %}

    <div class="headhand clearfix">
        Last check : <span id="last_check_date">{{ last_check }}</span>
        <small id="ajax_enabled"></small>
    </div>

    <div id="host_header">
        <div class="row-fluid">
            <div class="span1">
                {% if 'MAC' == host_os %}
                    <img src="img/logos/Apple_logo.png" alt="Apple" />
                {% elif 'UBUNTU' == host_os %}
                    <img src="img/logos/Ubuntu_logo.png" alt="Ubuntu" />
                {% elif 'DEBIAN' == host_os %}
                    <img src="img/logos/Debian_logo.png" alt="Debian" />
                {% endif %}
            </div>
            <div class="span11">
                <div class="hostname">{{ hostname }}</div>
                <div class="hostversion">{{ os_name }} {{ os_version }}</div>
            </div>
        </div>
    </div>

    <div class="alert hide">
        <strong>Indev Version</strong><br />
        This is an indev version. Only for developers right now. You can meet bug everywhere, say hello to them ;-)
    </div>

    <noscript>
        <div id="div_ajax_available_alert" class="alert alert-info">
            <a href="#" class="close" data-dismiss="alert">&times;</a>
            <strong>Dynamic refresh is not available on your web browser</strong><br />
            Please enable Javascript or try a more powerful web browser like Firefox, Chrome or Safari.
        </div>
    </noscript>


    <div id="div_ajax_error_alert" class="alert alert-error hide">
        An error occured
    </div>

    <div class="row-fluid">
        <div class="span4">
            <div class="dashboard-box">
                <div class="dashboard-box-headhand">
                    {% set cpu_status = '' %}

                    {% if cpu_alert is defined %}
                        {% set cpu_status = 'dashboard-box-status-alert' %}
                    {% elif cpu_warning is defined %}
                        {% set cpu_status = 'dashboard-box-status-warning' %}
                    {% elif cpu_ok is defined %}
                        {% set cpu_status = 'dashboard-box-status-ok' %}
                    {% endif %}

                    <div id="div_cpu_status" class="{{ cpu_status }}"></div>
                    <div class="dashboard-box-title">
                        CPU (used)
                    </div>
                </div>

                <div class="dashboard-box-datas" id="div_cpu_box">
                    {% if cpu_percent is undefined %}
                        <div class="title">Not checked</div>
                    {% else %}
                        <div class="title">
                            <span id="span_cpu_percent_value">{{ cpu_percent }}</span> %
                        </div>
                        <div class="subtitle">
                            <span id="span_cpu_user_value">{{ cpu_user }}</span> % user - <span id="span_cpu_system_value">{{ cpu_system }}</span> % system
                        </div>

                        {% set cpu_status = 'dashboard-box-status' %}

                        {% if cpu_alert is defined %}
                            {% set cpu_status = 'progress-danger' %}
                        {% elif cpu_warning is defined %}
                            {% set cpu_status = 'progress-warning' %}
                        {% elif cpu_ok is defined %}
                            {% set cpu_status = 'progress-success' %}
                        {% endif %}

                        <div id="div_cpu_progress" class="progress progress-striped {{ cpu_status }}">
                            <div id="bar_cpu_percent" class="bar" style="width:{{ cpu_percent }}%;"></div>
                        </div>
                    {% endif %}
                </div>

            </div>
        </div>

        <div class="span4">
            <div class="dashboard-box">
                <div class="dashboard-box-headhand">
                    {% set memory_status = 'dashboard-box-status' %}

                    {% if memory_alert is defined %}
                        {% set memory_status = 'dashboard-box-status-alert' %}
                    {% elif memory_warning is defined %}
                        {% set memory_status = 'dashboard-box-status-warning' %}
                    {% elif memory_ok is defined %}
                        {% set memory_status = 'dashboard-box-status-ok' %}
                    {% endif %}

                    <div id="div_memory_status" class="{{ memory_status }}"></div>
                    <div class="dashboard-box-title">Memory (used)</div>
                </div>
                <div class="dashboard-box-datas" id="div_memory_box">
                    {% if memory_percent is undefined %}
                        <div class="title">Not checked</div>
                    {% else %}
                        <div class="title">
                            <span id="span_memory_percent_value">{{ memory_percent }}</span> %
                        </div>
                        <div class="subtitle">
                            <span id="span_memory_used_value">{{ memory_used }}</span> used and
                            <span id="span_memory_free_value">{{ memory_free }}</span> free
                        </div>

                        {% set memory_status = '' %}

                        {% if memory_alert is defined %}
                            {% set memory_status = 'progress-danger' %}
                        {% elif memory_warning is defined %}
                            {% set memory_status = 'progress-warning' %}
                        {% elif memory_ok is defined %}
                            {% set memory_status = 'progress-success' %}
                        {% endif %}

                        <div id="div_memory_progress" class="progress progress-striped {{ memory_status }}">
                            <div id="bar_memory_percent" class="bar" style="width:{{ memory_percent }}%;"></div>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="span4">
            <div class="dashboard-box">
                <div class="dashboard-box-headhand">
                    {% set swap_status = '' %}

                    {% if swap_alert is defined %}
                        {% set swap_status = 'dashboard-box-status-alert' %}
                    {% elif swap_warning is defined %}
                        {% set swap_status = 'dashboard-box-status-warning' %}
                    {% elif swap_ok is defined %}
                        {% set swap_status = 'dashboard-box-status-ok' %}
                    {% endif %}

                    <div id="div_swap_status" class="{{ swap_status }}"></div>
                    <div class="dashboard-box-title">Swap (used)</div>
                </div>
                <div class="dashboard-box-datas" id="div_swap_box">
                    {% if 'undefined' == swap_configuration %}
                        <div class="title">No swap</div>
                    {% elif 'unlimited' == swap_configuration %}
                        <div class="title">
                            <span id="span_swap_used_value">{{ swap_used }}</span>
                        </div>
                        <div class="subtitle">
                            <span id="span_swap_percent_value">{{ swap_percent }}</span> % of physical memory
                        </div>
                    {% elif 'limited' == swap_configuration %}
                        <div class="title">
                            <span id="span_swap_used_value">{{ swap_used }}</span>
                        </div>
                        <div class="subtitle">
                            <span id="span_swap_percent_value">{{ swap_percent }}</span> % of
                            <span id="span_swap_size_value">{{ swap_size }}</span>
                        </div>

                        {% set swap_status = '' %}

                        {% if swap_alert is defined %}
                            {% set swap_status = 'progress-danger' %}
                        {% elif swap_warning is defined %}
                            {% set swap_status = 'progress-warning' %}
                        {% elif swap_ok is defined %}
                            {% set swap_status = 'progress-success' %}
                        {% endif %}

                        <div id="div_swap_progress" class="progress progress-striped {{ swap_status }}">
                            <div id="bar_swap_percent" class="bar" style="width:{{ swap_percent }}%;"></div>
                        </div>
                    {% else %}
                        <div class="title">Not available</div>
                    {% endif %}

                </div>
            </div>
        </div>

    </div>

    <div class="row-fluid">
        <div class="span4">
            <div class="dashboard-box">
                <div class="dashboard-box-headhand">
                    {% set load_status = '' %}

                    {% if load_alert is defined %}
                        {% set load_status = 'dashboard-box-status-alert' %}
                    {% elif load_warning is defined %}
                        {% set load_status = 'dashboard-box-status-warning' %}
                    {% elif load_ok is defined %}
                        {% set load_status = 'dashboard-box-status-ok' %}
                    {% endif %}

                    <div id="div_load_status" class="{{ load_status }}"></div>
                    <div class="dashboard-box-title">Load Average</div>
                </div>
                <div class="dashboard-box-datas" id="div_load_box">
                    {% if loadaverage is undefined %}
                        <div class="title">Not checked</div>
                    {% else %}
                        <div class="title">
                            <span id="span_load_value">{{ loadaverage }}</span>
                        </div>
                        <div class="subtitle">
                            <span id="span_load_percent_value">{{ loadaverage_percent }}</span> % of {{ cpu_count }} cores
                        </div>

                        {% set progress_class = '' %}

                        {% if load_alert is defined %}
                            {% set progress_class = 'progress-danger' %}
                        {% elif load_warning is defined %}
                            {% set progress_class = 'progress-warning' %}
                        {% elif load_ok is defined %}
                            {% set progress_class = 'progress-success' %}
                        {% endif %}

                        <div id="div_load_progress" class="progress progress-striped {{ progress_class }}">
                            <div id="bar_load_percent" class="bar" style="width:{{ loadaverage_percent }}%;"></div>
                        </div>
                    {% endif %}
                    </div>
                </div>
            </div>

        <div class="span8">
            <div class="dashboard-box">
                <div class="dashboard-box-headhand">
                    <div class="dashboard-box-status-ok"></div>
                    <div class="dashboard-box-title">Uptime</div>
                </div>
                <div class="dashboard-box-text" id="div_uptime_box">
                    {% if loadaverage is undefined %}
                        <div class="title">Not checked</div>
                    {% else %}
                        <div class="title">
                            <span id="span_uptime_full_text">{{ uptime }}</span> <small>(<span id="span_uptime_seconds_value">{{ uptime_seconds }}</span> seconds)</small>
                        </div>
                        <div class="subtitle">
                            Boot date : <span id="span_uptime_start_date_value">{{ start_date }}</span>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <div class="row-fluid">
        <div class="span12">
            <div id="div_disks_box" class="dashboard-box">
                <div class="dashboard-box-headhand">
                    <div class="dashboard-box-status-ok"></div>
                    <div class="dashboard-box-title">Disks</div>
                </div>
                <div class="dashboard-box-text">
                    {% if disks is undefined %}
                        <div class="title">Not checked</div>
                    {% else %}
                        <table class="table table-striped table_inline">
                            <tbody>
                                {% for disk in disks %}
                                    <tr>
                                        <td width="33%"><strong>{{ disk.name }}</strong></td>
                                        <td width="33%">{{ disk.free }} free / {{ disk.total }} total ({{ disk.percent }} % used)</td>
                                        <td width="33%">
                                            <div class="progress progress-striped progress-success">
                                                <div class="bar" style="width:{{ disk.percent }}%;"></div>
                                            </div>
                                        </td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <div class="headhand headhand-center clearfix">
        <a href="dashboard">Go to old full report</a>
    </div>
{% endblock %}

{% block bottom_javascript %}
    <script type="text/javascript" src="js/cr.ajax.js"></script>
{% endblock %}

{% block footer_version %}CentralReport Unix/Linux {{ CR_version }} - {{ CR_version_name }}{% endblock %}
