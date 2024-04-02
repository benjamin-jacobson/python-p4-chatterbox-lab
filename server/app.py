from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():

    if request.method == 'GET':
        messages = [m.to_dict() for m in Message.query.all()]
        return make_response(messages, 200)

    elif request.method == 'POST':
        # new_message = Message(
        #     body = 'test' #request.form.get("body"),
        #     username = 'testuser' #request.form.get("username"),
        #     created_at = datetime.datetime.now()
        #      )

        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(),201)

@app.route('/messages/<int:id>', methods = ['GET','PATCH','DELETE'])
def messages_by_id(id):

    if request.method == 'GET':
        message = Message.query.filter_by(id=id).first()
        return make_response(message.to_dict(),200)

    elif request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data.get(attr))
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        return make_response(message_dict,200)

    elif request.method == "DELETE":
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()
        return make_response({'message':'record successfully deleted'},200)







if __name__ == '__main__':
    app.run(port=5555)
