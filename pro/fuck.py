from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import Form
import json
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask('__main__')



