"""
main file which runs the flask app
import other components into this file
"""

from flask import Flask
app = Flask(__name__)

import todata.views

if __name__ == "__main__":
    app.run()