from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask('__main__',template_folder='./')
bootstrap = Bootstrap(app)

category_list = {'Social':0, 'Envrionment':0, 'People':0}

app.config['SECRET_KEY'] = "What is this?"

@app.route('/categories/')
def categories():
    return jsonify( category_list)
    #return render_template("categories.html", cat_list = category_list)


@app.route('/user/<name>',methods = ['POST','GET'])
def user(name):
    if request.method == 'GET':
        return render_template('user.html',name = name)
    else:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('delete from user_data where user=?',(name,))
        connection.commit()
        return redirect(url_for('index'))



@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        print("here top")
        return render_template('index.html')
    else:
        name = request.form['username']
        pwd = request.form['password']
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('insert into user_data (user, password) values (?,?)',(name, pwd))
        connection.commit()

        return redirect(url_for("user", name = name))


if __name__ == '__main__':    
    connection = sqlite3.connect('database.db')
    app.run(debug=True)

