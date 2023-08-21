from flask import Flask, render_template, request

from flask_pymongo import pymongo

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')

DBurl = 'mongodb+srv://Jai:jai123@trialpymongo.cqz8i2q.mongodb.net/'
client = pymongo.MongoClient(DBurl)

db = client.get_database('shipmnts')

user = db.users


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
        
        email_found = user.find_one({"email":email})

        if email_found:
            print("Already Exists")
            return render_template('home.html')
        if pass1 != pass2:
            print("Password Does Not Match")
            return render_template('home.html')

        else:
            user_input = {'uname':uname,'email':email, 'password':pass1}
            user.insert_one(user_input)
            # idhar khuch logged in render karvana hai

    return render_template('home.html')

@app.route('/Login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        
        email_found = user.find_one({"email":email})

        if email_found:
            email_val = email_found['email']
            pass_val = email_found['password']
            if pass_val == pass1:
                print("Logged In Successfully")
            else:
                print("Invalid Password")
        else:
            print("email not found")
    
    return render_template('home.html')

@app.route('/myQuestions')
def myQuestions():
    return render_template('personalQuestions/pQuestions.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)