from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)
from flask_app.models.log_and_reg_model import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def show_login():
    return render_template('login.html')

# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/loginuser', methods=['POST'])
def loginuser():
    login_data = { 'email' : request.form['email']}
    user_in_db = User.GetUserByEmail(login_data)

    #this accounts for if GetUserByEmail() returns the False value back
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect ('/login')
    #if email exists, now check pw by unhashing then comparing
    #two arguments, first one is what is the hashed pw, second is what we compare it to
    if not bcrypt.check_password_hash(user_in_db.password, request.form['loginpassword']):
        flash('Invalid Email/Passwordssssss')
        return redirect ('/login')

    session['user_id'] = user_in_db.id

    return redirect(f'/success/{user_in_db.id}')

@app.route('/register_user', methods = ['POST'])
def successful_registration():
    if not User.validate_user(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #hash version of our password

    newUser_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.CreateUser(newUser_data)     #when this executes, mysqlconnection will return back an ID, so we can set that equal to an ID and use it
    #can no longer use request.form bc we want the hash version of our pw, no longer satisfactory
    #so we will define a dictionary, then specify where pw comes from
    
    
    session['user_id'] = user_id                #whenever we successfully register/login, we want the user id stored somewhere, we can use session for that
    

    return redirect(f'/success/{user_id}')

# ====================================
# Log In Validations Route
# ====================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================

@app.route('/success/<int:user_id>')
def show_success(user_id):
    if 'user_id' not in session:        #must be successfully registered or logged in to make it here
        return redirect('/')
    newUser = User.GetUserById({'user_id': user_id})           #Selecting all from users, fetching info by ID, returning one object by ID
    return render_template('success.html', newUser=newUser)


# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================