
from flask import Flask, render_template, request, render_template_string
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask('temperatures')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'glowlicensefree'
app.config['MYSQL_PASSWORD'] = 'themeduckpioneer'
mysql = MySQL(app)

safe = True

@app.route('/name')
def view_selected():
    name = request.args['name']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('USE temperatures')
    try:
        if safe == False:
            query = 'SELECT * FROM project where name=\'{}\''.format(name)
            print(query)
            cursor.execute(query)
            data = list(cursor.fetchall())
            return render_template('table.html', data = data)
        if safe == True:
            cursor.execute('SELECT * FROM project where name=%s', (name,))
            print(name)
            data = list(cursor.fetchall())
            return render_template('table.html', data = data)
    except Exception as e:
        return str(e)

@app.route('/')
def view_all():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('USE temperatures')
    cursor.execute('SELECT * FROM project order by temp_id desc limit 1')
    data = list(cursor.fetchall())
    
    return render_template('table.html', data = data)

@app.route('/save')
def save_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('USE test_app')
    try:
        if safe == False:
            query = 'INSERT INTO project (name, temperature) VALUES (\'{}\', {})'.format(request.args['name'], request.args['temperature'])
            print('Query: {}'.format(query))
            cursor.execute(query)
            mysql.connection.commit()
            return 'ok'
        if safe == True:
            cursor.execute('INSERT INTO project (name, temperature) VALUES (%s, %s)', (request.args['name'], request.args['temperature'],))
            mysql.connection.commit()
            return 'ok'
    except Exception as e:
        return str(e)

@app.route('/cos')
def cos():
	godzina= request.args.get('id')
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('USE temperatures')
	try:
            cursor.execute('SELECT * FROM project where temp_id like %s', (godzina,))
            data = list(cursor.fetchall())
            return render_template('table.html', data = data)
	except Exception as e:
		return str(e)
@app.route('/all')
def sa():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('USE temperatures')
    cursor.execute('SELECT * FROM project')
    data = list(cursor.fetchall())
    return render_template('table.html', data = data)


if __name__ == '__main__': 
    app.run(host='0.0.0.0')
