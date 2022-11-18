from flask import (
    Blueprint,
    render_template,
)

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')


@main.errorhandler(500)
def handle_errors(error):
    return 'Not found!'
