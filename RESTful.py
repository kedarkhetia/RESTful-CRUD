from flask import *
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

auth = HTTPBasicAuth()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile.sqlite3'
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column("id", db.INTEGER, primary_key=True)
    name = db.Column("name", db.String(20))
    technology = db.Column("technology", db.String(20))

    def __init__(self, iden, name, technology):
        self.id = iden
        self.name = name
        self.technology = technology


@app.route('/', methods=['POST'])
def hello_world():
    return 'Hello World!'


@auth.verify_password
def login(username, password):
    if username=="admin" and password=="admin":
        return jsonify({"Status":"Login Successful"})


@auth.error_handler
def unauthorised():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/Read_Profile', methods=['GET'])
@auth.login_required
def read_profile():
    profile = []
    for p in Profile.query.all():
        profile.append({
            "id": p.id,
            "Name": p.name,
            "Technology": p.technology
        })
    return jsonify(profile)


@app.route('/Add_Profile', methods=['POST'])
@auth.login_required
def add_profile():
    p = Profile(request.json['id'], request.json['Name'], request.json['Technology'])
    db.session.add(p)
    db.session.commit()
    return jsonify({"Status": "Added"})


@app.route('/Update_Profile', methods=['PUT'])
@auth.login_required
def update_profile():
    iden = request.json['id']
    try:
        name = request.json['Name']
    except:
        name=None
    try:
        technology = request.json['Technology']
    except:
        technology=None
    modify = Profile.query.filter_by(id=iden).first()
    if name:
        modify.name = name
    if technology:
        modify.technology = technology
    db.session.commit()
    return jsonify({"Status": "Updated"})


@app.route('/Delete_Profile', methods=['DELETE'])
@auth.login_required
def delete_profile():
    iden = request.json['id']
    modify = Profile.query.filter_by(id=iden).first()
    db.session.delete(modify)
    db.session.commit()
    return jsonify({"Status": "Deleted"})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000, host='0.0.0.0')
