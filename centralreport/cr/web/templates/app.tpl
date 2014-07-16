{% extends "layout/base.layout.tpl" %}

{% block title %}{{ hostname }} dashboard - CentralReport{% endblock %}

{% block head_styles %}
    <link rel="stylesheet" href="static/css/centralreport.css">
{% endblock %}

{% block head_javascript %}
    <script type="text/javascript" src="static/js/centralreport.js"></script>
{% endblock %}

{% block body_class %}ng-app="crApp"{% endblock %}

{% block body %}
<div id="wrapper">

    <div ng-controller="LeftMenuCtrl">
        <div class="navbar navbar-default navbar-fixed-top" role="navigation">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" ng-click="isCollapsed = !isCollapsed">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">CentralReport Host</a>
                </div>
                <ul class="nav navbar-top-links navbar-right">
                </ul>
        </div>

        <div class="navbar-left navbar-static-side" role="navigation">
            <div class="sidebar-collapse collapse" collapse="isCollapsed">
                <cr-left-menu></cr-left-menu>
            </div>
        </div>
    </div>

    <div id="page-wrapper" class="extended" ng-view>
        <div class="row">
            <h3>Loading {{ hostname }} data for you...</h3>
        </div>
    </div>
</div>
{% endblock %}


