from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    render_template
)
from luks.hosts import ServerHosts


hosts = Blueprint('hosts', __name__)
host_svc = ServerHosts()


def is_api_request(req: request) -> bool:
    return req.path.startswith('/api/')


@hosts.route('/api/hosts/reload', methods=['GET'])
@hosts.route('/hosts/reload', methods=['GET'])
def reload_hosts():
    host_svc.reload()
    return redirect('/hosts')


@hosts.route('/api/hosts', methods=['GET'])
@hosts.route('/hosts', methods=['GET'])
def all_hosts():
    hosts_list = host_svc.all_hosts
    if is_api_request(request):
        return jsonify({'data': hosts_list})
    return render_template('hosts_table.html', hosts_list=hosts_list)


@hosts.route('/api/host', methods=['GET'])
@hosts.route('/host', methods=['GET'])
def get_host():
    """Simple GET all hosts with static IPs"""
    host_name = request.args.get('name', default=None, type=str)
    ip = request.args.get('ip', default=None, type=str)
    result = []
    if host_name is not None:
        result.append(host_svc.get_ip(host_name))
    elif ip is not None:
        result.append(host_svc.get_host(ip))

    return jsonify({'data': result})
