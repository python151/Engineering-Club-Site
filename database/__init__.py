def submit(tableName, variableList):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    variableList1 = []
    for i in variableList:
        variableList1.append(sec.sanitize(i))
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
        listOfRows.append(sec.sanitize(row))
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