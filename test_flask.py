from flask import Flask 
from flask_restplus import Api, Resource, fields
from sqlalchemy_db import db_op
db_object = db_op()
app = Flask(__name__)
api = Api(app, version="1.0", title="Name Recorder", description="Manage names of various users of the application")

user_model = api.model('User', {
     'id': fields.Integer(required=True, description='Id of user'),
     'username': fields.String(required=True, description='Username'),
     'password': fields.String(required=True, min_length=5, description='User password')
 })


@api.route('/user')
class Users(Resource):
    def get(self):
        return db_object.get_all_users()

    @api.expect(user_model)
    def post(self):
        data = api.payload
        return db_object.insert_data(data)


@api.route('/<username>')
@api.param('username', 'The User identifier')
class SingleUser(Resource):
    @api.doc('get a user')
    def get(self, username):
        return db_object.get_a_user(username)


if __name__ == '__main__':
    app.run(debug=True)
