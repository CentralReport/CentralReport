<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>{% block title %}CentralReport{% endblock %}</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/bootstrap-responsive.min.css">

    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/style-responsive.css">

    <link rel="stylesheet" href="css/custom.css">

    <script type="text/javascript" src="js/jquery.js"></script>

    {% block head_javascript %}{% endblock %}

</head>
<body>
    {% block body %}{% endblock %}
</body>
</html>
