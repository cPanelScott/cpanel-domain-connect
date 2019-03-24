from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/v2/<domain>/settings")
def discovery( domain ):
    return "Hello World moe! %s" % domain
