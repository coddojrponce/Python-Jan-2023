from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.post import Post

@app.route('/posts')
def all_posts():
    return render_template("all_posts.html",posts = Post.getAll())