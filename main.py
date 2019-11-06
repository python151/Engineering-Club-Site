from flask import Flask, request, render_template, redirect, jsonify, session
import sqlite3
import hashlib
import random
import database


#add documentation
#I can't read this code :(
class sec:
    # this will sanitize any inputs
    def sanitize(listOfPoints, characters=['abcdefghijklomnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ1234567890']):
        refinedData = ''
        for point in listOfPoints:
            if point in characters:
                refinedData = refinedData + point
        return refinedData



class routes(): #add pages to our app
    app = Flask(__name__)

    
    #this runs before every request
    @app.before_request
    def log():
        userIp = request.remote_addr
        session['ip_address'] = userIp
    

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
        return render_template("who.html")

    @app.route('/admin_login')
    def adminLogin():
        return render_template('adminLogin.html')

# these scan the user session and return pages acordingly
    @app.route('/learn')
    def howto():
        if session.get('logged_in'):
            group = session.get('group')
            database.get('group')
            return render_template('learn.html', group=group)
        elif not session.get('logged_in'):
            return redirect('/login')

    @app.route('/todolist')
    def todo():
        database.createTable('todo', [['rowid', 'INTEGER PRIMARY_KEY AUTO_INCREMENT'], ['name', 'TEXT'], ['content', 'TEXT'], ['groupName', 'TEXT'], ['dummy', 'TEXT']])
        group = session.get('group')
        conn, c = database.setup()
        c.execute('SELECT rowid, name, content  FROM todo WHERE content ="'+str(group)+'"')
        return render_template('todo.html', todo=c.fetchall())


    @app.route('/Comment', methods=["GET", "POST"])
    @app.route('/comment', methods=["GET", "POST"])
    def comment():
        if request.method == "POST" and session.get('logged_in'):
            database.createTable("comments", [['comment', "TEXT"], ['email', "TEXT"]])
            database.submit("comments", [request.form['comment'], session.get('email')])
            return redirect("/Home")
        elif session.get('logged_in') and request.method == 'GET':
            return render_template("comment.html")
        else:
            return render_template('mustLogin.html')


# these are forms taken in and functions called from the front end
    @app.route('/login1/', methods=["POST"])
    def get_data():
        if request.method == "POST":
            admin=False
            email = request.form.get("email")
            password = request.form.get("password")
            database.createTable('accounts', [['email', "TEXT"], ['hashedPassword', "TEXT"], ['salt', 'INTEGER'], ['names', 'TEXT'], ['age', 'TEXT'], ["groupOfUser", 'TEXT'], ["id", "INTEGER PRIMARY_KEY AUTO_INCREMENT"]])
            conn, c = database.setup()#actPassword = database.get("email", email, "accounts", "hashedPassword, salt")
            c.execute("SELECT hashedPassword, salt FROM accounts WHERE email = '"+email+"'")
            actPassword = str(c.fetchone()).replace("('", "").replace("',", ",").replace(')', "").split(", ")
            print(actPassword[0])
            try:
                hashed_password = hashlib.sha512(password.encode('utf-8') + actPassword[1].encode('utf-8')).hexdigest()
            except:
                hashed_password = "none"
            print(hashed_password)
            if hashed_password == actPassword[0] or admin: #hashed_password == actPassword[0]:
                c.execute("SELECT age FROM accounts WHERE email='"+email+"'")
                name = str(c.fetchall()[0]).replace("',)", '').replace("('", '')
                session['errors'] = ""
                session['name'] = name
                c.execute('SELECT id FROM accounts WHERE email = "'+email+'"')
                group = str(c.fetchall()[0]).replace("',)", '').replace("('", '')
                session['admin'] = admin
                session['group'] = group
                session['logged_in'] = True
                return jsonify('home')
            elif actPassword[0] == 'None':
                session['errors'] = "Account Does Not Exist"
                return jsonify('signup')
            else:
                session['errors'] = "Password Incorrect"
                return jsonify('login')
       
    @app.route('/signup1/', methods=['POST'])
    def signUp():
            database.createTable('accounts', [['email', "TEXT"], ['hashedPassword', "TEXT"], ['salt', 'INTEGER'], ['names', 'TEXT'], ['age', 'TEXT'], ['groupOfUser', 'TEXT'], ["id", "INTEGER PRIMARY_KEY AUTO_INCREMENT"]])
            email = request.form.get("email")
            conn, c = database.setup()
            c.execute("SELECT id FROM accounts WHERE email = '"+email+"'")
            if not c.fetchall():
                password = request.form.get("password")
                name = request.form.get("name")
                age = request.form.get("age")
                group = request.form.get("group")
                salt = str(random.randint(10000, 99999))
                hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
                database.submit('accounts', [email, hashed_password, salt, name, age, group])
                session['admin'] = False
                session['name'] = name
                session['group'] = group
                session['logged_in'] = True
                return jsonify('home')
            return jsonify('login')

    @app.route('/logout/')
    def logout():
        session['logged_in'] = False
        session['group'] = "None"
        session['admin'] = False
        session['name'] = "Not Logged In"
        return redirect('home')
    
    @app.route('/adminLogin/', methods=['POST'])
    def adminLoginForm():
        if request.method == 'POST':
            request.form.get('email')




    @app.route('/addtodo/', methods= ['POST'])
    def addtodo():
        if session.get('logged_in') and session.get('admin'):
            database.createTable('todo', [['rowid', 'INTEGER PRIMARY_KEY AUTO_INCREMENT'], ['name', 'TEXT'], ['content', 'TEXT'], ['groupName', 'TEXT'], ['dummy', 'TEXT']])
            name = request.form.get('name')
            content = request.form.get('content')
            group = request.form.get('group')    
            database.submit('todo', [name, content, group ,'sd'])
            return jsonify('Success!')
        else:
            return jsonify('login')

    @app.route('/del/', methods=['POST'])
    def deltodo():
        if session.get('logged_in'):
            group = session.get('group')
            name = request.form.get('name')
            print(name)
            conn, c = database.setup()
            c.execute('SELECT dummy FROM todo WHERE rowid = "navbar"')
            print(c.fetchall())
            c.execute('DELETE FROM todo WHERE rowid = "'+name+'" and content = "'+group+'"')
            conn.commit()
            return jsonify('todolist')
        return jsonify('login')





    @app.errorhandler(500) #error page for internal server errors '500'
    def err500(e):
        return render_template("error.html", error=e)

    @app.errorhandler(404) #error page for missing resource errors '404'
    def err404(e):
        return render_template("error.html", error=e)



    if __name__ == '__main__':
        app.secret_key=bytes(random.randint(99999999, 999999999))
        app.run(host='0.0.0.0', port=8000)
        
flaskApp = routes
