from flask import Flask, render_template, request, render_template_string
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask('temperatures')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'glowlicensefree'
app.config['MYSQL_PASSWORD'] = 'themeduckpioneer'
mysql = MySQL(app)

@app.route('/')
def view_all():
	temp=request.args.get('temperature')
	print(temp)
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('USE temperatures')
	if (temp is None):
		cursor.execute('SELECT * FROM project order by temp_id desc limit 1')
		data = list(cursor.fetchall())
		return render_template('table.html', data = data)
	else:
		cursor.execute('SELECT * FROM project WHERE temperature = %s', (temp,))
		data = list(cursor.fetchall())
		return render_template('table.html',data=data)

@app.route('/all')
def sa():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('USE temperatures')
    cursor.execute('SELECT * FROM project')
    data = list(cursor.fetchall())
    return render_template('table.html', data = data)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404


if __name__ == '__main__': 
    app.run(host='0.0.0.0')
