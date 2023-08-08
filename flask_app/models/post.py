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
    # @classmethod
    # def getAll(cls):
    #     query="SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;"
    #     results = connectToMySQL(cls.db).query_db(query)
    #     # print(results)
    #     # for x in results:
    #     #     print("this is the dictionary")
    #     #     print(x)
    #     #     print("***********************\n")
    #     if not results:
    #         return []
    #     all_posts = []
    #     for row in results:
    #         # *******************************
    #         # post object is created
    #         this_post = cls(row)

    #         # *******************************
    #         # *******************************
    #         # We need to create a user object to attach to the post
    #         data={
    #                 'id':row['users.id'],
    #                 'first_name':row['first_name'],
    #                 'last_name':row['last_name'],
    #                 'email':row['email'],
    #                 'password':row['password'],
    #                 'created_at':row['users.created_at'],
    #                 'updated_at':row['users.updated_at'],
    #             }
    #         # We attach the user object to the post on their self.owner attribute
    #         this_post.owner = user.User(data)
    #         # Now we add it to a list we can send back
    #         all_posts.append(this_post)
    #     return all_posts



    @classmethod
    def getAll(cls):
        query="SELECT * FROM posts LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON likes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_posts = []
        # for row in results:
        #     all_posts.append(cls(row))
        # return all_posts
        if not results:
            return []
        this_post=None
        for row in results:

            if this_post == None:
                this_post = cls(row)
                all_posts.append(this_post)

            elif not this_post.id == row['id']:
                this_post = cls(row)
                all_posts.append(this_post)

            if not row['post_id'] == None:
                
                data={
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
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
    def get_one(cls,id):
        data={
            "id":id
        }
        query="SELECT * FROM posts LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON likes.user_id = users.id WHERE posts.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)

    
        if not results:
            return []
        this_post = cls(results[0])
        for row in results:
            
            if not row['post_id'] == None:
                
                data={
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at'],
                }
                this_user = user.User(data)
                this_post.likes.append(this_user)
        return this_post

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