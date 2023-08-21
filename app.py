from flask import Flask, render_template

from flask_pymongo import pymongo

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')

# DBurl = ''
# client = pymongo.MongoClient(DBurl)

# db = client.get_database('trialDatabase')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)