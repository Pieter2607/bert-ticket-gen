from flask import Flask, request, render_template, url_for

website = Flask(__name__)

###############################################################
#                           Routes                            #
###############################################################

@website.route('/')
def index():
    return render_template('index.html')

@website.route('/ticket/get')
def get_ticket():
    return render_template('get_ticket.html')