from flask_app import app

#import controllers into server.py
#from flask_app.controllers import
from flask_app.controllers import log_and_reg_controller
#run pipenv install PyMySQL flask flask-bcrypt
#Remember save .mwb file to folder


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.