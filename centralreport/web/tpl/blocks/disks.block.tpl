<div class="dashboard-box-headhand">
    <div class="dashboard-box-status-ok">

    </div>
    <div class="dashboard-box-title">
        Disks
    </div>
</div>
<div class="dashboard-box-text">
    {% if disks is undefined %}
    <div class="title">
        Not checked
    </div>
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
