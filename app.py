from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from functools import wraps
import jwt
import uuid


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
bcrypt = Bcrypt(app)
CORS(app)


@app.route("/test")
def test():
    return "test"


@app.route("/login")
def login():
    token = jwt.encode({
        "subject":"foo",
        "role":"admin"
    }, app.config["SECRET_KEY"])
    
    return jsonify({"token":token})
    

@app.route("/")
def index():
    secret = request.args["secret"]
    verify = request.args["verify"]

    code = str(uuid.uuid4())
    code_id = code.split("-")[0]
    
    pw_hash = bcrypt.generate_password_hash(secret)
    check_hash = bcrypt.check_password_hash(pw_hash, verify)
    
    res = {
       "id":code_id,
       "hash":str(pw_hash),
       "ck_hash":check_hash
    }
    
    return jsonify(res)
    
    
app.run(host="127.0.0.1", debug=True)    