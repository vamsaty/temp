from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import Form
import json
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask('__main__',template_folder='./')
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = "What is this?"  

@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']
         
    return redirect(url_for(index))


@app.route('/api/v1/users/<name>',methods=['POST','DELETE'])
def rem_user(name):
    if request.method == 'POST':
        session.pop('user')
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('delete from user_data where user=?',(name,))
        connection.commit()
        return redirect(url_for('index'))

    return render_template('remove.html',name = name)

@app.route('/api/v1/users', methods = ['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['username']
            pwd = request.form['password']
            session['user'] = name
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute("insert into user_data(user,password) values (?,?)", (name,pwd))
            connection.commit()
            connection.close()
            return redirect(url_for('rem_user',name = name))
            
        except sqlite3.IntegrityError:
            return redirect(url_for('index'))

    return render_template('register.html', info = session.get('user'))


@app.route('/api/v1/categories',methods = ['GET'])
def categories():
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        names = list(cursor.execute('select name from category_data').fetchall())
        freqs = list(cursor.execute('select num_acts from category_data').fetchall())
        connection.close()
        final = {}
        for i in range(0,len(names)):
            final[ str( names[i][-1] ) ] = str( freqs[i][-1] )

        return jsonify(final)


@app.route('/api/v1/categories',methods = ['POST'])
def categories():


@app.route('/index/', methods = ['GET', 'POST'])
def index():
    lf = 0
    lv = None
    if 'user' in session:
        lf = 1
        lv = session['user']
    else:
        lf = 0
    return render_template('index.html',log_flag = lf, name = lv)


if __name__ == '__main__':    
    connection = sqlite3.connect('database.db')
    app.run(debug=True)

