import re
from flask_app import bcrypt, DATABASE
from flask import flash
from flask_app.config.my_sql_connection import connectToMySQL
import sys
sys.dont_write_bytecode = True

# ------# ADDED  # ------#

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        # ------# EDITED per table columns  # ------#
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# ----  CREATE - REGISTERS NEW USER  ----

    @classmethod
    def create_user(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        print(data)
        return connectToMySQL(DATABASE).query_db(query, data)

# ----  FIND USER BY EMAIL  ----

    @classmethod
    def find_by_email(cls, data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False


# ----  FIND USER BY ID  ----

    @classmethod
    def find_by_id(cls, data):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results[0])
        if results and len(results) < 1:
            return False
        else:
            # found_user = cls(results[0])
            # print(found_user.first_name)
            return results[0]


#  -------  VALIDATE LOGIN  ---------

    @classmethod
    def validate_login(cls, data):

        found_user = cls.find_by_email(data)

        if not found_user:
            flash("Invalid Login!")
            return False
            # This compares pw_hash & unhashed password #
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            return False

        return found_user

#  -------  VALIDATION METHOD  ---------
    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent the user

#  -------  VALIDATE FORM DATA  ---------

    @staticmethod
    def validate_data(data):
        is_valid = True  # we assume this is true
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Please enter a VALID email address.")
            is_valid = False
        elif User.find_by_email(data):
            flash("Email already registered!")
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash("Passwords do not match.")
            is_valid = False
        print("IS VALID ==========>", is_valid)
        return is_valid
