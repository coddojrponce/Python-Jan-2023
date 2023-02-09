from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.user import User


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dash():
    if "user_id" not in session:
        return redirect("/")
    return render_template("dash.html",users=User.getAll())

@app.route("/submit",methods=["POST"])
def submit():
    # print(request.form)
    if request.form["action"] == "register":
        # Run our registration logic
        data={
            "f_name":request.form["f_name"].lower(),
            "l_name":request.form["l_name"].lower(),
            "email":request.form["email"].lower(),
            "password":request.form["password"]
        }

    
        user_id = User.save(data)
        print(f"This is the user id: {user_id}")
        session["user_id"]=user_id
        return redirect("/dashboard")

    else:

        this_user = User.getOneByEmail({'email':request.form['email'].lower()})
        print("This is the user")
        print(this_user)
        if this_user:
            if request.form["password"] == this_user.password:
                session["user_id"] = this_user.id
                return redirect("/dashboard")
            else:
                return redirect("/")


        return redirect("/")

@app.route('/users/<int:id>/edit')
def updateView(id):
    return render_template("update.html",user=User.getOne({'id':id}))

@app.route('/users/<int:id>')
def userView(id):
    return render_template("one_user.html",user=User.getOne({'id':id}))

@app.route("/users/<int:id>/update",methods=["POST"])
def update(id):
    data={
            "id":id,
            "f_name":request.form["f_name"].lower(),
            "l_name":request.form["l_name"].lower(),
            "email":request.form["email"].lower(),
            "password":request.form["password"]
    }

    User.update(data)

    return redirect("/dashboard")

@app.route("/users/<int:id>/destroy")
def destroy(id):
    User.destroy({'id':id})
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

