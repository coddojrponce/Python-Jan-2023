from flask import Flask,render_template,redirect,request,session
from flask_app import app
from flask_app.controllers import user,post,like


if __name__ == "__main__":
    app.run(debug=True)
