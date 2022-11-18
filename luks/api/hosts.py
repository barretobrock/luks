from flask import (
    Blueprint,
    Request,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
)

from luks.hosts import ServerHosts

hosts = Blueprint('hosts', __name__)
host_svc = ServerHosts()


def is_api_request(req: Request) -> bool:
    return req.path.startswith('/api/')


@hosts.route('/api/hosts/reload', methods=['GET'])
@hosts.route('/hosts/reload', methods=['GET'])
def reload_hosts():
    host_svc.reload()
    if is_api_request(request):
        return make_response('', 200)
    return redirect('/hosts')


@hosts.route('/api/hosts', methods=['GET'])
@hosts.route('/hosts', methods=['GET'])
def all_hosts():
    hosts_list = host_svc.all_hosts
    if is_api_request(request):
        return jsonify({'data': hosts_list})
    return render_template(
        'render_datatable.html',
        tbl_id_name='hosts-table',
        order_list=[2, "asc"],
        header_maps={
               'Name': {'col': 'name', 'copyable': True},
               'Type': {'col': 'machine_type'},
               'IP':  {'col': 'ip', 'copyable': True}
           },
        reload_endpoint='hosts.reload_hosts',
        results_list=hosts_list,
        last_update=host_svc.get_hosts_modified_time()
    )


@hosts.route('/api/host', methods=['GET'])
@hosts.route('/host', methods=['GET'])
def get_host():
    """Simple GET all hosts with static IPs"""
    host_name = request.args.get('name', default=None, type=str)
    ip = request.args.get('ip', default=None, type=str)
    hosts_list = []
    if host_name is not None:
        hosts_list.append(host_svc.get_ip(host_name))
    elif ip is not None:
        hosts_list.append(host_svc.get_host(ip))
    if is_api_request(request):
        return jsonify({'data': hosts_list})
    return render_template(
        'render_datatable.html',
        tbl_id_name='hosts-table',
        order_list=[2, 'asc'],
        header_maps={
               'Name': {'col': 'name', 'copyable': True},
               'Type':  {'col': 'machine_type'},
               'IP':  {'col': 'ip', 'copyable': True}
           },
        reload_endpoint='hosts.reload_hosts',
        results_list=hosts_list,
        last_update=host_svc.get_hosts_modified_time()
    )
