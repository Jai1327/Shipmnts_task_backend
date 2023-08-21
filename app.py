import datetime
from flask import Flask, render_template, request, session

from flask_pymongo import pymongo

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

DBurl = 'mongodb+srv://Jai:jai123@trialpymongo.cqz8i2q.mongodb.net/'
client = pymongo.MongoClient(DBurl)

db = client.get_database('shipmnts')

userDB = db.users
questionDB = db.questions


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ["GET","POST"])
def register():
    uname = request.form.get("uname")
    email = request.form.get('email')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')

    if request.method == "POST":
        uname = request.form.get("uname")
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')

        if(not uname or not email or not pass1 or not pass2):
            print("Error")
            return render_template('home.html')
        
        email_found = userDB.find_one({"email":email})

        if email_found:
            print("Already Exists")
            return render_template('home.html')
        if pass1 != pass2:
            print("Password Does Not Match")
            return render_template('home.html')

        else:
            user_input = {'uname':uname,'email':email, 'password':pass1}
            userDB.insert_one(user_input)
            # idhar khuch logged in render karvana hai

    return render_template('home.html')

@app.route('/Login', methods = ["GET","POST"])
def login():
    message = ''
    session.permanant = False
    if "email" in session:
        print("Logged In")
        return render_template('home.html')
    if request.method == "POST":
        email = request.form.get('email')
        pass1 = request.form.get('pass1')

        if not email or not pass1:
            print("Enter all the details")
            return render_template('home.html')
        
        email_found = userDB.find_one({"email":email})

        if email_found:
            email_val = email_found['email']
            pass_val = email_found['password']
            if pass_val == pass1:
                session.permanent = False
                session["email"] = email_val
                print("Logged In Successfully")
            else:
                print("Invalid Password")
        else:
            print("email not found")
    
    return render_template('home.html')

@app.route('/postQuestion')
def postQuestion():
    if request.method == "POST":
        question = request.form.get('question')
        email = request.form.get('email')
        timeStamp = datetime.datetime.now()
        
        userInput = {"email":email, "timestamp": timeStamp,"question:":question,
                     "upvotes":0,"downvotes":0,"comments":{}}
        questionDB.insert_one(userInput)

@app.route('/deletePost', methods=["GET","POST"])
def deletePost():
    if request.methd == "POST":
        email = request.form.get('email')
        timestamp = request.form.get('timestamp')
        post_found = questionDB.find_one({'email':email, "timestamp":timestamp})
        if post_found:
            questionDB.delete_one(post_found)
        else:
            print("Post Not Found")
            return 500
    return 200

@app.routes('/updatePost')
def updatePost():
    if request.method == "POST":
        email = request.form.get('email')
        timestamp = request.form.get('timestamp')
        questionUpdate = request.form.get('questionUpdate')
        query = {"email":email,"timestamp":timestamp}
        post_found = questionDB.find_one(query)

        if post_found:
            update = {"$set": {"question":questionUpdate}}
            questionDB.update_one(query,update)
        else:
            return 500
    return 200

@app.route('/upvote')
def upvote():

    return 200







        



if __name__ == '__main__':
    app.run(debug=True, port=8080)