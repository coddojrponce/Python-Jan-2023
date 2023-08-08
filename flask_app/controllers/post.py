from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.post import Post

@app.route('/posts')
def all_posts():
    return render_template("all_posts.html",posts = Post.getAll())


@app.route("/posts/<int:id>")
def view_one_post(id):
    return render_template("one_post.html",post=Post.get_one(id))