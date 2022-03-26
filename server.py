from flask import Flask, request, jsonify
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from functools import wraps
import uuid
import jwt

app = Flask(__name__)
app.config["SECRET_KEY"] = "llave_del_token"
bcrypt = Bcrypt(app)



def fn_deco(callback):
    @wraps(callback)
    def fn_internal(*args, **kargs):
        pw = "foo"
        token = "fook"
        
        if pw == token:
           return callback(*args, **kargs)
        else:
           return "block" 
    return fn_internal    


@app.route("/deco")
@fn_deco
def action():
    return "endpoint /deco"


@app.route("/gen_id")
def gen_uuid():
    code = str(uuid.uuid4())
    id = code.split("-")
    
    res = {
      "id":id[0],
      "name":"foo",
      "role":"admin" 
    }
    
    return jsonify(res)


@app.route("/gen_hash")
def gen_hash():
    des_secreto = "foo"
    secreto = bcrypt.generate_password_hash("foo")    
    check = bcrypt.check_password_hash(secreto, des_secreto)

    return jsonify({"check":str(check)})


@app.route("/gen_token")
def gen_jwt():
    profile = {
        "email":"foo@foo.com",
        "name":"foo"
    }
    token = jwt.encode(profile, app.config["SECRET_KEY"])
    return jsonify({"token":token})
    

@app.route("/profile")
@fn_deco
def profile():
    id = uuid.uuid4()
    password = bcrypt.generate_password_hash("password")
      
    profile = {
        "id":str(id),
        "email":"foo@foo.com",
        "name":"foo",
        "role":"admin",
        "password":str(password)
    }

    token = jwt.encode(profile, app.config["SECRET_KEY"])
    
    return jsonify({"profile":token})

app.run(host="127.0.0.1", debug=True)
