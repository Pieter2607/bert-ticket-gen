from crypt import METHOD_MD5
import random
import string
import qrcode
import hashlib
from PIL import Image
from flask import Flask, request, render_template, url_for


app = Flask(__name__)

# Define valid api keys
VALID_API_KEYS = {
    'DEVELOPMENTKEY',
    'MjzDH4wZ56BQnN2ZrGqqB3KCydTzfzQe',
    'eVpLyFyWzSpPeMLDGLn23wbsE7y9kgrj'
}

# Define symmetric key for checking data integrity
SYMMETRIC_KEY = b'A9b3RmDqX9Ly8xN6bUbnDD8nWHKLqdtTG9jocsx3WpckHLyinLmGZco8p5xjJKtE'


###############################################################
#                           Routes                            #
###############################################################

@app.route('/')
def index():
    """Serve homepage"""
    return render_template('index.html')


@app.route('/ticket/request')
def ticket_form():
    """Serve ticket form"""
    return render_template('ticket_form.html')


@app.route('/ticket/response', methods=['POST'])
def show_ticket():
    """Create and return a user's ticket"""
    date = request.form.get('date')
    train_id = request.form.get('train_id')
    ticket_nr = get_random_string(64)
    ticket_hash = hash(ticket_nr + date + train_id)
    ticket_qr_filename = create_qr_code(
        ticket_nr, date + train_id + ticket_hash)
    return render_template('ticket.html', ticket_date=date, ticket_train=train_id, ticket_nr=ticket_nr, ticket_qr_path=url_for('static', filename=ticket_qr_filename))


###############################################################
#                      Helper functions                       #
###############################################################

def get_random_string(length):
    """ Create random string with combination of lower and upper case characters"""
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    return result_str


def create_qr_code(ticket_id, extra_content):
    """Create qr code and save png to static folder and return filename"""
    filename = f'qr/{ticket_id}.png'
    img = qrcode.make(ticket_id + extra_content)
    img.save(f'static/{filename}')
    return filename


def hash(content):
    """Create hash using `content` and private key"""
    m = hashlib.sha256()
    m.update(content.encode('utf-8'))
    m.update(SYMMETRIC_KEY)
    return m.hexdigest()
