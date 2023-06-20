from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = 'login_and_registration'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
        is_valid = True
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(User.DB).query_db(query, data)
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please enter a valid email.')
            is_valid = False
        if len(results) >= 1:
            flash('Email is already taken.')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be 8 or more characters long!')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash ('Passwords did not match.')
            is_valid = False
        return is_valid

    # @staticmethod
    # def is_valid(email):
    #     is_valid = True
    #     query = """
    #     SELECT * FROM users
    #     WHERE email = %(email)s;
    #     """
    #     results = connectToMySQL(User.DB).query_db(email)
    #     if len(results) >= 1:
    #         flash('Email is already taken.')
    #         is_valid = False
    #     if not EMAIL_REGEX.match(new_user['email']):
    #         flash('Please enter a valid email.')
    #         is_valid = False
    #     return is_valid


    @classmethod
    def CreateUser(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def GetUserById(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def GetUserByEmail(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def DeleteUser(cls, user_id):
        query = """
        DELETE FROM users
        WHERE id = %(user_id)s;
        """
        data = {
            "id" : user_id
        }
        return connectToMySQL(cls.DB).query_db(query, data)
    
    