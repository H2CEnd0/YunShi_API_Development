# -*- coding: utf-8 -*-
from flask import Flask
from apps.Hospital_Api.Hospital_Api import yunshi
from apps.bupa.PD_Voice_APP import bupa
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.debug = False
app.register_blueprint(yunshi, url_prefix='/yunshi')
app.register_blueprint(bupa, url_prefix='/bupa')

if __name__ == '__main__':
    app.run()