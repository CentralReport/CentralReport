<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}CentralReport{% endblock %}</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {% block head_styles %}{% endblock %}
    {% block head_javascript %}{% endblock %}

</head>
<body {% block body_class %}{% endblock %}>
    {% block body %}{% endblock %}

    {% block bottom_javascript %}{% endblock %}
</body>
</html>
