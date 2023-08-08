from flask_app import app
from flask import render_template,session,redirect,request,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

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
        is_valid=User.validate_user(request.form)
        if not is_valid:
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        print("**************** This is the hash **** ")
        data={
            "first_name":request.form["first_name"].lower(),
            "last_name":request.form["last_name"].lower(),
            "email":request.form["email"].lower(),
            "password": pw_hash
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
            if len(request.form['password']) < 8:
                flash("Password must be at least 8 characters")
                return redirect("/")
            if bcrypt.check_password_hash(this_user.password, request.form['password']):
                session["user_id"] = this_user.id
                return redirect("/dashboard")
            else:
                flash("Incorrect Password")
                return redirect("/")
        else:
            flash("No user with this email")
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
            "first_name":request.form["first_name"].lower(),
            "last_name":request.form["last_name"].lower(),
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
