from flask_app import app

from flask_app.controllers import user_controller, recipe_controller

import sys
sys.dont_write_bytecode = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')