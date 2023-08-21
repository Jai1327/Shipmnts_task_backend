import datetime
from flask import Flask, jsonify, render_template, request, session
import constant

from flask_pymongo import pymongo

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = constant.secretKey

# DBurl = 'mongodb+srv://Jai:jai123@trialpymongo.cqz8i2q.mongodb.net/'
client = pymongo.MongoClient(constant.dbURL)

db = client.get_database(constant.dbName)

userDB = db.users
questionDB = db.questions


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ["GET","POST"])
def register():
    message = ''
    status = ''
    statusCode = ''

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
            message = "Enter all the details"
            status = "Fail"
            statusCode = 400
            return jsonify({"message":message,"status":status}), statusCode
        
        email_found = userDB.find_one({"email":email})

        if email_found:
            print("Already Exists")
            message = "Email Already Exists"
            status = "Fail"
            statusCode = 400
            # return jsonify({/"message":,"status":"Fail"})
        elif pass1 != pass2:
            print("Password Does Not Match")
            message = "Passwords Do Not Match"
            status = "Fail"
            statusCode = 400
            # return jsonify({"message":"","status":"Fail"})

        else:
            user_input = {'uname':uname,'email':email, 'password':pass1}
            userDB.insert_one(user_input)
            message = "Logged In Successfully"
            status = "Pass"
            statusCode = 200

    return jsonify({"message":message,"status":status}), statusCode

@app.route('/Login', methods = ["GET","POST"])
def login():
    message = ''
    status = ''
    statusCode = 200
    if request.method == "POST":
        email = request.form.get('email')
        pass1 = request.form.get('pass1')

        if not email or not pass1:
            print("Enter all the details")
            message = 'Enter All the details'
            status = 'Fail'
            statusCode = 400
            return jsonify({"message":message,"status":status}), statusCode

        email_found = userDB.find_one({"email":email})

        if email_found:
            email_val = email_found['email']
            pass_val = email_found['password']
            if pass_val == pass1:
                message = "Logged In Successfully"
                status = "Pass"
                # session.permanent = False
                # session["email"] = email_val
                print("Logged In Successfully")
            else:
                message = "Incorrect Password"
                status = "Fail"
                statusCode = 400
                print("Invalid Password")
        else:
            message = "Email Not Found"
            status = "Fail"
            statusCode = 400
            print("email not found")
        return jsonify({"message":message,"status":status}), statusCode
    

@app.route('/postQuestion', methods = ["GET","POST"])
def postQuestion():
    if request.method == "POST":
        question = request.form.get('question')
        email = request.form.get('email')
        timeStamp = datetime.datetime.now()
        
        userInput = {"email":email, "timestamp": timeStamp,"question:":question,
                     "upvotes":0,"downvotes":0,"comments":{}}
        questionDB.insert_one(userInput)
        return jsonify({"message":"Successfully posted a question", "status":"Pass"}), 200
    return jsonify({"message":"Unexpected Error Occured", "status":"Fail"})

@app.route('/deletePost', methods=["GET","POST"])
def deletePost():
    if request.methd == "POST":
        message = ''
        status = ''
        statusCode = 200
        email = request.form.get('email')
        timestamp = request.form.get('timestamp')
        post_found = questionDB.find_one({'email':email, "timestamp":timestamp})
        if post_found:
            questionDB.delete_one(post_found)
            message = 'Post Found and Deleted'
            status = 'Pass'
        else:
            print("Post Not Found")
            message = 'Post Not Found'
            status = 'Fail'
            statusCode = 400
    return jsonify({"message":message,"status":status}), statusCode

@app.routes('/updatePost', methods = ["GET","POST"])
def updatePost():
    message = ''
    status = ''
    statusCode = 200
    if request.method == "POST":
        email = request.form.get('email')
        timestamp = request.form.get('timestamp')
        questionUpdate = request.form.get('questionUpdate')
        query = {"email":email,"timestamp":timestamp}
        post_found = questionDB.find_one(query)

        if post_found:
            update = {"$set": {"question":questionUpdate}}
            questionDB.update_one(query,update)
            message = 'Post Updated Successfully'
            status = "Pass"
        else:
            message = "Post Not found"
            status = "Fail"
            statusCode = 400
    return jsonify({"message":message,"status":status}), statusCode

@app.route('/getAllQuestion',methods = ["GET","POST"])
def getQuestion():
    allQuestion = questionDB.find()
    return allQuestion

@app.route('/getMyQuestion',methods = ["GET","POST"])
def getQuestion():
    if request.method == "POST":
        email = request.form.get('email')
        allQuestion = questionDB.find({"email": email})
    return allQuestion



@app.route('/upvote')
def upvote():

    return 200

@app.route('/downvote')
def upvote():

    return 200

@app.rout('/comment')
def comment():
    return 200






        



if __name__ == '__main__':
    app.run(debug=True, port=8080)