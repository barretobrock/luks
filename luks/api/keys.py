import json
import pathlib
from flask import (
    Blueprint,
    redirect,
    request,
    make_response,
    jsonify,
    render_template
)
from diceware import generate_phrase
from luks.secrets import (
    Secrets,
    get_secret_file,
    Entry
)
from luks.forms import KeyGenForm


keys = Blueprint('keys', __name__)

# Get password for secrets database
password = get_secret_file()
secrets = Secrets(password)


def is_api_request(req: request) -> bool:
    return req.path.startswith('/api/')


@keys.route('/api/keys', methods=['GET'])
@keys.route('/keys', methods=['GET'])
def all_keys():
    x: Entry
    keys_list = [{
        'title': x.title,
        'updated': x.mtime.astimezone()
    } for x in secrets.db.entries if not x.title.startswith('hidden-')]
    if is_api_request(request):
        return jsonify({'data': keys_list})
    return render_template('keys_table.html', keys_list=keys_list)


@keys.route('/api/keys/reload', methods=['GET'])
@keys.route('/keys/reload', methods=['GET'])
def reload_keys():
    secrets.load_database(password)
    if is_api_request(request):
        return make_response('', 200)
    return redirect('/keys')


@keys.route('/api/key/<key_name>', methods=['GET'])
@keys.route('/key/<key_name>', methods=['GET'])
def get_key(key_name: str):
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
        return render_template('keygen_results.html', phrase_list=phrases)
    else:
        # Render form to filter results
        form = KeyGenForm()
        return render_template('keygen.html', form=form, template='form-template')
