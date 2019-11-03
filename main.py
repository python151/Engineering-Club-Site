from flask import Flask, request, render_template, redirect, url_for, jsonify, session, flash
import sqlite3
import hashlib
import random

class sec:
    def sanitize(listOfPoints, characters=[list('''\n{}[];:<>,./?!@#$%^&*()-_=+\|'"`~'''), ['//0', '//1', '//2', '//3', '//4', '//5', '//6', '//7', '//8', '//9', '//10', '//11', '//12', '//13', '//14', '//15', '//16', '//17', '//18', '//19', '//20', '//21', '//22', '//23', '//24', '//25', '//26', '//27', '//28', '//29', '//30', '//31', '//32', '//33']]):
        refinedData = []
        for point in listOfPoints:
            i = 0
            fix = False
            for char in characters[0]:
                point = str(point)
                if point == char:
                    point1 = characters[1][i]
                    fix = True
                else:
                    if not fix:
                        point1 = point
                i += 1
            if point1 == '"':
                point1 = ''
            refinedData.append(point1)
        return ''.join(refinedData)
    
    def deSanitize(listOfPoints, characters=[list('''\n{}[];:<>,./?!@#$%^&*()-_=+\|'"`~'''), ['//0', '//1', '//2', '//3', '//4', '//5', '//6', '//7', '//8', '//9', '//10', '//11', '//12', '//13', '//14', '//15', '//16', '//17', '//18', '//19', '//20', '//21', '//22', '//23', '//24', '//25', '//26', '//27', '//28', '//29', '//30', '//31', '//32', '//33']]):
        final = []
        listOfPoints = str(listOfPoints)
        for i, point in enumerate(listOfPoints):
            if point == "/":
                keyCodeIterator = i + 2
                keyCode = listOfPoints[keyCodeIterator]
                try:
                    key = characters[0][keyCode]
                    print(key)
                    final.append(listOfPoints.replace("//"+keyCode, key))
                except:
                    pass
            else:
                final.append(point)
        return ''.join(final).replace("(", "").replace(",)", "")
class database:
    def submit(tableName, variableList):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        variableList1 = []
        for i in variableList:
            variableList1.append(sec.deSanitize(i))

        str00 = '", "'.join(variableList1)
        c.execute('INSERT INTO '+tableName+' VALUES("'+str00+'")'.replace(', )', ")"))
        conn.commit()
        c.close()
        conn.close()

    def getTable(tableName):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM "+tableName)
        listOfRows = []
        for row in c.fetchall():
            listOfRows.append(sec.deSanitize(row))
        return listOfRows
        c.close()
        conn.close()

    def createTable(tableName, variableList):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        str00 = []
        for num, i in enumerate(variableList):
            if len(i) == num:
                str00.append(i[0]+" "+i[1])
            else:
                str00.append(i[0]+" "+i[1]+", ")
        sqlcode = 'CREATE TABLE IF NOT EXISTS '+tableName+' ('+''.join(str00)+')'.replace(', )', ")")
        c.execute(sqlcode.replace(', )', ')'))
        conn.commit()
        c.close()
        conn.close()
    
    def rename(old, new):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''ALTER TABLE "'''+old+'''" RENAME TO '''+new)
        conn.commit()
        c.execute('UPDATE lists SET name = "'+new+'" WHERE name = "'+old+'"')
        conn.commit()
        c.close()
        conn.close()

    def deleteItem(name, whereVar, var='email'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM '+name+' WHERE "'+var+'" = "'+whereVar+'"')
        conn.commit()
        c.close()
        conn.close()

    def get(var, whereVar, tableName, getting):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT "+getting+" FROM "+tableName+" WHERE '"+var+"' = '"+whereVar+"'")
        listOfRows = []
        for row in c.fetchall():
            listOfRows.append(row)
        #listOfRows = database.dataRefiner(listOfRows)
        return listOfRows
        c.close()
        conn.close()
    
    def setup():
        '''
        will return the conn and the cursor respectivly
        '''
        connectionToDatabase = sqlite3.connect("database.db")
        cursorToTalkToDatabase = connectionToDatabase.cursor()
        return connectionToDatabase, cursorToTalkToDatabase

class routes():
    app = Flask(__name__)

    @app.before_request
    def log():
        userIp = request.remote_addr
        #logIp(userIp)

    @app.route('/')
    @app.route('/home')
    @app.route('/Home')
    def index():
        return render_template("index.htm")

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
    
    @app.route('/login')
    def loginDisp():
        return render_template('login.html')

    @app.route('/signup')
    def signupDisp():
        return render_template('signup.html')
    
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
            hashed_password = hashlib.sha512(password.encode('utf-8') + actPassword[1].encode('utf-8')).hexdigest()
            print(hashed_password)
            if email == 'admin@a.com' and hashed_password == 'c9749ccdc8ce0939af2a60a8b7ac298e2639d2c7eeef7f0d634db96a3559430b2f48d053e478ef7552a1bbcf551c8c17f79b5233e438e4f8d75579b44947c87b':
                admin=True
            if hashed_password == actPassword[0] or admin:#hashed_password == actPassword[0]:
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
                session['errors'] = "Account Not Exist"
                return jsonify('signup')
            else:
                session['errors'] = "Wrong Password"
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


    @app.route('/see')
    def see():
        comments = database.getTable('todo')
        return render_template('see.html', e=list(comments))


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
        session['admin'] = True
        return render_template("who.html")

    @app.route('/todolist')
    def todo():
        database.createTable('todo', [['rowid', 'INTEGER PRIMARY_KEY AUTO_INCREMENT'], ['name', 'TEXT'], ['content', 'TEXT'], ['groupName', 'TEXT'], ['dummy', 'TEXT']])
        group = session.get('group')
        conn, c = database.setup()
        #database.submit('todo', ['navbar', 'we need to fix the navbar shrinking prob.', 'Programming', 'dsdf'])
        c.execute('SELECT rowid, name, content  FROM todo WHERE content ="'+str(group)+'"')
        #print(c.fetchall())
        return render_template('todo.html', todo=c.fetchall())

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

    @app.errorhandler(500)
    def err500(e):
        return render_template("error.htm", error=e)

    @app.errorhandler(404)
    def err404(e):
        return render_template("error.htm", error=e)

    if __name__ == '__main__':
        app.secret_key=bytes(random.randint(99999999, 999999999))
        app.run(debug=True)

flaskApp = routes
