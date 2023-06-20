from flask import Flask, render_template, redirect, session, request  # Import Flask to allow us to create our app, if u need render_template


app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = 'pug' 	#key goes into here