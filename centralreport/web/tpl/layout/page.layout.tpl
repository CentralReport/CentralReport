{% extends "layout/base.layout.tpl" %}

{% block body %}
    <div class="container">
        <div class="page-header clearfix">
            {% block header_title %}CentralReport host dashboard{% endblock %}
            <small>{% block header_subtitle %}{% endblock %}</small>
        </div>

        <div class="content">
            {% block content %}<h1>No data to display</h1>{% endblock %}
        </div>
    </div>

    <div class="footer">
        {% block footer_version %}CentralReport Unix/Linux{% endblock %}<br />
        Visit <a href="http://www.github.com/miniche/CentralReport" target="_blank">Github</a> for more information
    </div>
{% endblock %}

