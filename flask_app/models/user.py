from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = "facenote"

    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.posts=[]
        self.likes=[]

    @classmethod
    def getAll(cls):
        query="SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_users = []
        for row in results:
            print("KEYKEYKEYKEYKEYKEYEYKEY")
            for key in row.keys():
                print(key)
            all_users.append(cls(row))
        return all_users
    @classmethod
    def save(cls,data):
        query ="INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def getOneByEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if results:
            this_user = cls(results[0])
            # print("This is the results")
            # print(results)
            # print("this is the results[0]")
            # print(results[0])
            for row in results:
                print("KEYKEYKEYKEYKEYKEYEYKEY")
                for key in row.keys():
                    print(key)
                if row['user_id'] == None:
                    break
                data={
                    "id":row["posts.id"],
                    "image":row["image"],
                    "comment":row["comment"],
                    "created_at":row["posts.created_at"],
                    "updated_at":row["posts.updated_at"]
                }
                this_user.posts.append(post.Post(data))
            return this_user
        return False

    @classmethod
    def update(cls,data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s,password=%(password)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def destroy(cls,data):
        query="DELETE FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name'] ) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(data['last_name'] ) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email'] ):
            flash("Invalid Email")
            is_valid = False
        if len(data['password'] ) < 8:
            flash("Password must be 8 characters or longer")
            is_valid = False
        return is_valid