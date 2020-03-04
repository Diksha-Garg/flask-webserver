from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,insert,select,exc,VARCHAR
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
key = "secure"
class db_op:

    def __init__(self):
        engine = create_engine('mysql+pymysql://root@localhost/test_db')
        self.connection = engine.connect()
        print(self.connection)
        meta = MetaData()
        self.students = Table(
                    'students', meta,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(32)),
                    Column('password', VARCHAR(256)),
                )
        meta.create_all(engine)
    def encrypt_password(self,password):
        cipher = encrypt(key, password)
        encoded_cipher = b64encode(cipher)
        return encoded_cipher

    def decrypt_password(self,e_password):
        cipher = b64decode(e_password)
        plaintext = decrypt(key, cipher)
        return plaintext

    def insert_data(self, data):
        encrypted_password = self.encrypt_password(data['password'])
        print(str(encrypted_password))
        query = insert(self.students).values(id=data['id'], username=data['username'], password=encrypted_password)
        try:
            result_obj = self.connection.execute(query)
            return {
                'status': 'success',
                'message': 'Successfully registered.'
            }
        except exc.IntegrityError:
            print("user with this ID already exists")
            return {
                'status': 'fail',
                'message': "User with id already exists"
            }

    def user_data_format(self, result_list):
        result_format = []
        for x in result_list:
            result_format.append({'id': x[0], 'username': x[1]})
        return result_format

    def get_all_users(self):
        query = select([self.students])
        result_obj = self.connection.execute(query)
        result_set = result_obj.fetchall()
        return self.user_data_format(result_set)

    def get_a_user(self, name):
        try:
            query = select([self.students]).where(self.students.columns.username == name)
            result_obj = self.connection.execute(query)
            result_set = result_obj.fetchall()
            if not result_set:
                raise Exception("Invalid Username")
            print(result_set[0][2])
            output = self.user_data_format(result_set)
            output[0].update({'password': self.decrypt_password(result_set[0][2]).decode('utf-8')})
            return output
        except Exception as e:
            print(e)
            return {
                'status': 'fail',
                'message': e.args
            }

