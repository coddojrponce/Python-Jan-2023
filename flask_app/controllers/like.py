from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.post import Post

@app.route('/like/<int:id>',methods=["POST"])
def like_post(id):
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(session['user_id'])
    data={
        'user_id':int(session['user_id']),
        'post_id':id
    }
    Post.like(data)
    return redirect("/posts")