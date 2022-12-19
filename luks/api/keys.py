import json
import pathlib

from diceware import generate_phrase
from flask import (
    Blueprint,
    Request,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
)

from luks.forms import KeyGenForm
from luks.secrets import (
    Entry,
    Secrets,
    get_secret_file,
)

keys = Blueprint('keys', __name__)


def get_secrets() -> Secrets:
    return Secrets(get_secret_file())


def is_api_request(req: Request) -> bool:
    return req.path.startswith('/api/')


@keys.route('/api/keys', methods=['GET'])
@keys.route('/keys', methods=['GET'])
def all_keys():
    secrets = get_secrets()
    x: Entry
    keys_list = [{
        'title': x.title,
        'updated': x.mtime.astimezone()
    } for x in secrets.db.entries if not x.title.startswith('hidden-')]
    if is_api_request(request):
        return jsonify({'data': keys_list})
    return render_template('render_datatable.html',
                           tbl_id_name='keys-table',
                           order_list=[1, "desc"],
                           header_maps={
                               'Name': {
                                   'col': 'title',
                                   'path': '/key/%s',
                                },
                               'Last Update': {
                                   'col': 'updated'
                               },
                           },
                           reload_endpoint='keys.reload_keys',
                           results_list=keys_list)


@keys.route('/api/keys/reload', methods=['GET'])
@keys.route('/keys/reload', methods=['GET'])
def reload_keys():
    secrets = get_secrets()
    secrets.load_database(get_secret_file())
    if is_api_request(request):
        return make_response('', 200)
    return redirect('/keys')


@keys.route('/api/key/<key_name>', methods=['GET'])
@keys.route('/key/<key_name>', methods=['GET'])
def get_key(key_name: str):
    secrets = get_secrets()
    entry = secrets.get_entry(key_name)
    if entry is None:
        return {}
    if any([x is not None for x in [entry.username, entry.password]]):
        resp = {
            'un': entry.username,
            'pw': entry.password
        }
    else:
        resp = {}
    resp.update(entry.custom_properties)
    if len(entry.attachments) > 0:
        for att in entry.attachments:
            # For attachments, try to decode any that we might expect. For now, that's just JSON
            if isinstance(att.data, bytes):
                # Decode to string, try loading as json
                resp[att.filename] = json.loads(att.data.decode('utf-8'))
    if is_api_request(request):
        return jsonify({'data': [resp]})
    secret_dict = {key_name: resp}
    return render_template('key_detail.html', key_dict=secret_dict)


@keys.route('/keys/keygen', methods=['GET', 'POST'])
def generate_keys():
    if request.method == 'POST':
        # Load words
        with pathlib.Path.home().joinpath('data', 'wordlist.txt').open() as f:
            words = [x.strip() for x in f.readlines()]
        form = request.form
        phrases = generate_phrase(
            word_list=words,
            n_phrases=form.get('n_phrases', 10, type=int),
            n_words=form.get('n_words', 6, type=int),
            char_limit=form.get('char_limit', 32, type=int),
            joiner=form.get('joiner_char', '-'),
            symbols=form.get('symbols', '!@#$%_^&*')
        )
        phrases = [{'val': x, 'len': len(x)} for x in phrases]
        return render_template(
            'render_datatable.html',
            tbl_id_name='keygen-results',
            order_list=[1, "desc"],
            header_maps={
                'Result': {
                    'col': 'val',
                    'copyable': True
                },
                'Len': {
                    'col': 'len'
                }
            },
            results_list=phrases
        )
    else:
        # Render form to filter results
        form = KeyGenForm()
        if len(request.args) > 0:
            # If URL params were added to the request, bypass form generation and go straight to POST
            #   render results
            form.n_phrases.data = int(request.args.get('phrz', 10))
            form.n_words.data = int(request.args.get('wrds', 6))
            form.char_limit.data = int(request.args.get('charlim', 32))
        return render_template('keygen.html', form=form, template='form-template')
