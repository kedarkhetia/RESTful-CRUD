from flask import *

app = Flask(__name__)

profile = [

    {
        'id': 1,
        'Name': 'Kedar Khetia',
        'Technology': 'Python'
    },
    {
        'id': 2,
        'Name': 'Dhyey Moliya',
        'Technology': 'ReactJs'
    }

]


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/Read_Profile/', methods=['POST'])
def read_profile():
    return jsonify(profile)


@app.route('/Add_Profile/', methods=['POST'])
def add_profile():
    new_profile = {
        'id': profile[-1]['id'] + 1,
        'Name': request.json['Name'],
        'Technology': request.json['Technology']
    }
    profile.append(new_profile);
    return '{"Status":"Added"}'


@app.route('/Update_Profile/', methods=['Post'])
def update_profile():
    iden = request.json['id']
    name = request.json['Name']
    tech = request.json['Technology']
    for i in profile:
        if i['id'] == iden:
            if name:
                i['Name'] = name
            elif tech:
                i['Technology'] = tech
            return '{"Status":"Updated"}'


@app.route('/Delete_Profile/', methods=['Post'])
def delete_profile():
    iden = request.json['id']
    for i in profile:
        if i['id'] == iden:
            profile.pop(i)
            break
    return '{"Status":"Deleted"}'

if __name__ == '__main__':
    app.run()
