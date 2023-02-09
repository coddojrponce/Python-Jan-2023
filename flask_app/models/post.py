from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Post:
    db = "facenote"

    def __init__(self,data):
        self.id=data['id']
        self.image=data['image']
        self.comment=data['comment']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.likes=[]
        self.owner=None

    @classmethod
    def getAll(cls):
        query="SELECT * FROM posts LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON likes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_posts = []
        # for row in results:
        #     all_posts.append(cls(row))
        # return all_posts
        this_post=None
        for row in results:

            if this_post == None:
                this_post = cls(row)

            if not this_post.id == row['id']:
                all_posts.append(this_post)
                this_post = cls(row)
                
            if row['post_id'] == None:
                break
            data={
                'id':row['users.id'],
                'f_name':row['f_name'],
                'l_name':row['l_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],
            }
            this_user = user.User(data)
            this_post.likes.append(this_user)
        return all_posts

    @classmethod
    def save(cls,data):
        query ="INSERT INTO posts(image,comment) VALUES(%(image)s,%(comment)s);"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    

    @classmethod
    def getOne(cls,data):
        query="SELECT * FROM posts LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON likes.user_id = users.id WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update(cls,data):
        query="UPDATE posts SET image=%(image)s, comment=%(comment)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def destroy(cls,data):
        query="DELETE FROM posts WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def like(cls,data):
        query="INSERT INTO likes(user_id,post_id) VALUES(%(user_id)s,%(post_id)s);"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result