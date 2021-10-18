from flask import Blueprint


main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    return 'Main page!'


@main.errorhandler(500)
def handle_errors(error):
    return 'Not found!'
