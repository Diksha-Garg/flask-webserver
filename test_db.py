import mysql.connector
import sys


class db_op:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="test_db")
        except:
            print("database doesn't exist")
            sys.exit()
        print(self.mydb)

        create_table_query = 'CREATE TABLE users (username VARCHAR(255), password VARCHAR(255))'
        mycursor = self.mydb.cursor()
        try:
            mycursor.execute(create_table_query)
        except:
            print("Table with this name already exists")
    def fetch_user_exec(self,cmd):
        mycursor = self.mydb.cursor()
        mycursor.execute(cmd)
        my_result = mycursor.fetchall()
        output = []
        for x in my_result:
            output.append({'username': x[0], 'password': x[1]})
        return output
    def get_all_users(self):
        #print("Hello")
        list_usr = "SELECT * FROM users"
        return fetch_user_exec(list_usr)


    def insert_data(self, data):
        print(type(data['username']))
        mycursor = self.mydb.cursor()
        user_list = db_op.get_all_users(self)

        # print(len(self.output))
        try:
            for x in range(len(user_list)):
                #print(user_list[x]['username'])
                if user_list[x]['username'] == data['username']:
                    #print("HHello")
                    raise ValueError("Username already exists")

            sql_insert = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (data['username'], data['password'])

            mycursor.execute(sql_insert)

            self.mydb.commit()

            print(mycursor.rowcount, "record inserted.")
            return {
                'status': 'success',
                'message': 'Successfully registered.'
            }
        except Exception as e:
            print(repr(e))
            return {
            'status': 'fail',
            'message': 'User already exists. Please Log in.'
            }

    def get_a_user(self, name):
        
        sql_usrname = "SELECT * FROM users WHERE username = '{}'".format(name)
        return fetch_user_exec(sql_usrname)







