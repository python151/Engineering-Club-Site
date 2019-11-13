# importing dependencies
from flask import Flask, request, render_template, redirect, jsonify, session

import hashlib
import random
import os
import threading

import database
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool


#add documentation
#I can't read this code :(
class security:
    # this will sanitize any inputs
    def sanitize(self, listOfPoints, characters='abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ1234567890'):
        '''
        It takes in the string to sanatize and the characters to allow in the characters variable this variable will default to allow only letters and numbers
        '''
        refinedData = ''
        for point in listOfPoints:
            if point in characters:
                refinedData = refinedData + point
        return refinedData

# defining security object
sec = security()

#add pages to our app
app = Flask(__name__)


#this runs before every request
#logs user ip and updates breadcrum
@app.before_request
def log():
    userIp = request.remote_addr
    session['ip_address'] = userIp
    #session['breadcrum'] = str(session.get('breadcrum')) + request.endpoint


# this is a 'soft' function it just returns a template
@app.route('/')
@app.route('/home')
@app.route('/Home')
def index():
    return render_template("index.html")

@app.route('/login')
def loginDisp():
    return render_template('login.html')

@app.route('/signup')
def signupDisp():
    return render_template('signup.html')

@app.route('/Robot')
def robot():
    return render_template("robot.html")

@app.route('/Code')
def code():
    return render_template("code.html")

@app.route('/Marketing')
def marketing():
    return render_template("marketing.html")

@app.route('/Who Are We')
def who():
    hashed_password = hashlib.sha512(str("704605Mm").encode('utf-8') + str(939353).encode('utf-8')).hexdigest()

    # uploading account to database
    Base = declarative_base()
    engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    s=DBSession()
    new_person = database.AdminUsers(name="Matthew",
    password=hashed_password,
    salt=int(939353),
    email='dogm646@gmail.com',
    level=10)
    s.add(new_person)
    s.commit()

    return render_template("who.html")

@app.route('/admin_login')
def adminLogin():
    return render_template('adminLogin.html')



# these scan the user session and return pages acordingly

@app.route('/admin')
def admin():
    if session.get('logged_in') and session.get('admin'):
        return render_template('admin.html')
    else:
        return redirect('/admin_login')

# returns things to learn depending on group
@app.route('/learn')
def howto():
    if session.get('logged_in'):
        # setting up database session
        group = session.get('group')
        Base = declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        # getting things to learn (admins get all)
        if session.get('admin'):
            things = s.query([database.Learn])
        else:
            s.query([database.Learn]).filter(database.Learn.group == group)
        # rendering template with things variable
        return render_template('learn.html', things=things)
    elif not session.get('logged_in'):
        # if not logged in redirects to login
        return redirect('/login')

# this returns the to do list for the users group
@app.route('/todolist')
def todo():
    if session.get('logged_in'):
        # getting variables
        Base = declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        todolist = s.query(database.Todolist).filter(database.Todolist.group==session.get('group')).all()
        # rendering template with to do list
        return render_template('todo.html', todolist=todolist)
    else:
        # redirecting to login if not logged in
        return redirect('/login')

# these are forms taken in and functions called from the front end
# this is my login form
@app.route('/login1/', methods=["POST"])
def get_data():
    if request.method == "POST":
        # getting email and sanatizing it
        email = request.form.get("email")
        email = sec.sanitize(email, characters='abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ1234567890@.')

        # checking if its the account exists
        Base = declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        try:
            account = s.query(database.Account).filter(database.Account.email==email).one()
        except:
            return jsonify('signup')

        # getting the password and salt to hash then sanatizing the salt
        salt = str(account.salt)
        password = request.form.get("password")
        password = sec.sanitize(salt, characters='123456789')

        # hashing passwords and deleting old variables from RAM
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        del password
        del salt

        # if password is correct updates session variables and redirects you to home
        if hashed_password == account.password:
            # deleting hashed password from ram
            del hashed_password

            name = account.name
            group = account.group
            
            session['logged_in'] = True
            session['name'] = name
            session['group'] = group
            session['errors'] = ''

            return jsonify('home')
        else:
            # if password is wrong reloads the page
            session['errors'] = "Password Incorrect"
            return jsonify('login')
    
# signup form
@app.route('/signup1/', methods=['POST'])
def signUp():
    if request.method == 'POST':
        # getting and sanatizing email
        email = request.form.get("email")
        email = sec.sanitize(email, characters='abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ1234567890@.')

        # checking if account with email already exists
        Base = declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db',
        poolclass=SingletonThreadPool)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        try:
            s.query(database.Account).filter(database.Account.email==email).one()
            accountAlreadyExists = True
        except:
            accountAlreadyExists = False

        if not accountAlreadyExists:
            # getting form variables, generating salt, and sanatizing the retreived variables
            password = request.form.get("password")
            name = request.form.get("name")
            group = request.form.get("group")
            print(name, group)
            name = sec.sanitize(name)
            group = sec.sanitize(group)
            print(name, group)

            salt = str(random.randint(10000, 99999))

            # hashing password with salt
            hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

            # uploading account to database
            new_person = database.Account(name=name,
            password=hashed_password,
            salt=int(salt),
            email=email,
            group=group)
            s.add(new_person)
            s.commit()

            # updating session variables and logging in
            session['admin'] = False
            session['name'] = name
            session['group'] = group
            session['logged_in'] = True

            # redirecting to home
            return jsonify('home')
        elif  accountAlreadyExists:
            # if account already exists redirecting to login page
            return jsonify('login')

@app.route('/logout/')
def logout():
    # reseting session variables
    session['group'] = "None"
    session['admin'] = False
    session['name'] = "Log in"
    session['logged_in'] = False
    # redirecting you to home
    return redirect('/home')

# admin signup form
@app.route('/adminSignupForm/', methods=['POST'])
def adminSignUp():
    if request.method == 'POST':
        # getting credintials
        admin = session.get('admin')
        level = session.get('level')

        # checking credentials
        if admin and level == 10:
            # getting and sanatizing email
            email = request.form.get("email")
            email = sec.sanitize(email, characters='abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ1234567890@.')

            # checking if admin account with email already exists
            Base = declarative_base()
            engine = create_engine('sqlite:///mainDatabase.db',
            poolclass=SingletonThreadPool)
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            s=DBSession()
            try:
                s.query(database.AdminUsers).filter(database.AdminUsers.email==email).one()
                accountAlreadyExists = True
            except:
                accountAlreadyExists = False

            if not accountAlreadyExists:
                # getting form variables, generating salt, and sanatizing the retreived variables
                password = request.form.get("password")
                name = request.form.get("name")
                level = request.form.get("level")

                name = sec.sanitize(name)
                level = sec.sanitize(level, characters='0123456789')

                salt = str(random.randint(10000, 99999))

                # hashing password with salt
                hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

                # uploading account to database 
                new_person = database.AdminUsers(name=name,
                password=hashed_password,
                salt=int(salt),
                email=email,
                level=level)
                s.add(new_person)
                s.commit()

                # redirecting to admin page
                return jsonify('admin')
            elif  accountAlreadyExists:
                # if account already exists redirecting to login page
                return jsonify('admin_login')
        
# this is my admin login form
@app.route('/adminLogin/', methods=["POST"])
def adminLoginForm():
    if request.method == "POST":
        # getting email
        email = request.form.get("email")
        
        # checking if its the account exists
        Base = declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db', poolclass=SingletonThreadPool)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        try:
            account = s.query(database.AdminUsers).filter(database.AdminUsers.email == email).one()
        except:
            return jsonify('home')

        # getting the password and salt to hash
        salt = str(account.salt)
        password = request.form.get("password")

        # hashing passwords and deleting old variables from RAM
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        del password
        del salt

        # if password is correct updates session variables and redirects you to the admin page
        if hashed_password == account.password:
            # deleting hashed password from RAM
            del hashed_password

            name = account.name
            level = account.level
            
            session['logged_in'] = True
            session['admin'] = True
            session['level'] = level
            session['name'] = name
            session['group'] = 'admin'
            session['errors'] = ''

            return jsonify('admin')
        else:
            # if password is wrong reloads the page
            session['errors'] = "Password Incorrect"
            return jsonify('admin_login')



@app.route('/addtodo/', methods= ['POST'])
def addtodo():
    # checks if logged in as admin
    if session.get('logged_in') and session.get('admin'):
        # gets form variables
        name = request.form.get('name')
        content = request.form.get('content')
        group = request.form.get('group')

        # uploads to database
        Base=declarative_base()
        engine = create_engine('sqlite:///mainDatabase.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        s=DBSession()
        query = database.Todolist(group=group, itemName=name, itemContent=content)
        s.add(query)
        s.commit()

        # returns string
        return jsonify('Success!')
    else:
        # redirects to login if not logged in
        return redirect('/login')

@app.route('/del/', methods=['POST'])
def deltodo():
    if session.get('logged_in'):
        # getting name
        name = request.form.get('name')

        # checking if its in the database
        try:
            Base=declarative_base()
            engine = create_engine('sqlite:///mainDatabase.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            s=DBSession()
            s.query(database.Todolist).filter(database.Todolist.itemName == name).one()
        except:
            return jsonify('todolist')

        # getting group
        group = session.get('group')

        # deleting from database
        d = database.Todolist.delete().where(and_(database.Todolist.itemName == name, database.Todolist.group == group))
        s.execute(d)

        # clearing ram
        del group
        del name

        # returning redirect location
        return jsonify('todolist')
    return jsonify('login')





@app.errorhandler(500) #error page for internal server errors '500'
def err500(e):
    return render_template("error.html", error=e)

@app.errorhandler(404) #error page for missing resource errors '404'
def err404(e):
    return render_template("error.html", error=e)



if __name__ == '__main__':
    app.secret_key=bytes(random.randint(1, 99))
    app.run(debug=True, host='0.0.0.0', port=8000)
        

