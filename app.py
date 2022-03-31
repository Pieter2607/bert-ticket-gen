from flask import Flask, request, render_template, url_for

website = Flask(__name__)

###############################################################
#                           Routes                            #
###############################################################

@website.route('/')
def index():
    return render_template('index.html')