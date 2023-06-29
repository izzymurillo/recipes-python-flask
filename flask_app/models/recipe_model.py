import sys
sys.dont_write_bytecode = True

from flask_app import DATABASE

from flask_app.models.user_model import User

from flask import flash

from flask_app.config.my_sql_connection import connectToMySQL


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30mins = data['under_30mins']
        self.created_at  = data['created_at']
        self.updated_at  = data['updated_at']
        self.user_id = data['user_id']

# ----  CREATE - REGISTERS NEW USER  ----

    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipes (name, description, instructions, date_made, under_30mins,user_id)
            VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30mins)s,%(user_id)s);
        """
        print("DATA ==================>", data)

        return connectToMySQL(DATABASE).query_db(query, data)


# ------------ READ ALL - SHOW ALL RECIPES   ------------
    @classmethod
    def get_all(cls):

        query = """SELECT * FROM recipes
                JOIN users ON users.id = recipes.user_id
                ORDER BY name;
                """

        results = connectToMySQL(DATABASE).query_db(query)
        print("RESULTS ===============>", results)

        all_recipes = []

        for result in results:
            recipe = cls(result)

            user_data = {
                **result,
                'id' : result['users.id'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }

            # print("USER DATA ================>", user_data)

            recipe.owner = User(user_data)
            # print("RECIPE OWNER ====================>", recipe.owner)
            # print("RECIPE =================>", recipe)
            all_recipes.append(recipe)

        # print("ALL RECIPES =============>", all_recipes)
        return all_recipes


# ------------   READ ONE - SHOW ONE RECIPE   ------------
    @classmethod
    def get_one(cls, data):

        query = """SELECT * FROM recipes
                JOIN users ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """

        result = connectToMySQL(DATABASE).query_db(query, data)
        print ("RESULT (MODEL)==================>", result)    
        
        if result:
            # create an instance of the recipe
            this_recipe = cls(result[0])
            # create an instance of the user
            user_data = {
                **result[0],
                'id' : result[0]['users.id'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }

            this_user = User(user_data)

            this_recipe.creator = this_user
            print("RESULT2 (MODEL) ================>", result)
            return this_recipe
        return False


# ------------   EDIT (POST ROUTE)   ------------
    @classmethod
    def update(cls,data):

        query = """
            UPDATE recipes SET
            name = %(name)s,
            description = %(description)s,
            instructions = %(instructions)s,
            date_made = %(date_made)s,
            under_30mins = %(under_30mins)s
            WHERE id = %(id)s
        """

        return connectToMySQL(DATABASE).query_db(query, data)




# ------------   DELETE   ------------
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


#  -------  VALIDATE FORM DATA  ---------

    @staticmethod
    def validate_data(data):
        is_valid = True  # we assume this is true
        if len(data['name']) < 3:
            flash("Name field is required and must be at least 3 characters.")
            is_valid = False
        # if len(data['description']) < 3:
        #     flash("Description field is required and must be at least 3 characters.")
        #     is_valid = False
        # if len(data['instructions']) < 3:
        #     flash("instructions field must be at least 3 characters.")
        #     is_valid = False

        print("IS VALID ==========>", is_valid)
        return is_valid