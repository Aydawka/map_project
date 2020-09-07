from flask import Flask,render_template,flash,request,redirect,url_for,flash
from flask_mysqldb import MySQL


app=Flask(__name__)


app.secret_key = 'many random bytes'


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskcontacts'
app.config['MYSQL_CURSORCLASS']='DictCursor'


mysql=MySQL(app)

@app.route("/")
def index():
	cur=mysql.connection.cursor()
	cur.execute('SELECT * FROM contacts')
	data=cur.fetchall()
	return render_template("index.html",contacts=data)


@app.route("/add",methods=['GET','POST'])
def add_contact():
	if request.method == 'POST': 
		fullname=request.form['fullname']
		phone=request.form['phone']
		email=request.form['email']
		cur=mysql.connection.cursor()
		cur.execute('INSERT INTO contacts(fullname,phone,email) VALUES (%s,%s,%s)',(fullname,phone,email))
		mysql.connection.commit()
		flash('contact added')
		return redirect(url_for('index'))



@app.route("/edit/<id>")
def edit_contact(id):
	cur=mysql.connection.cursor()
	cur.execute('SELECT * FROM  contacts WHERE id={0}'.format(id))
	data=cur.fetchall()

	return render_template('edit.html',contact=data[0])


@app.route("/delete/<string:id>")
def delete_contact(id):
	cur=mysql.connection.cursor()
	cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
	mysql.connection.commit()
	flash('contact deleted')
	return redirect(url_for('index'))



if __name__=='__main__':
	app.run(debug=True)


