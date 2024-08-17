#!/usr/bin/env python3

from flask import Flask
from resources.account_resource import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)