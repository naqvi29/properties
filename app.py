from flask import Flask, render_template, request, url_for, jsonify, json, send_file, send_from_directory,session
import pymongo
import requests
import os, sys
import re
from bson.objectid import ObjectId

app = Flask(__name__)

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "properties"
db = client[database_name]

@app.route("/")
def hello_world():
    return render_template("index-9.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
       username = request.form.get("username")
       email = request.form.get("email")
       password = request.form.get("password")
       conf_password = request.form.get("conf_password")
       regex = '[^@]+@[a-zA-Z0-9]+[.][a-zA-Z]+'
       if not (re.search(regex, email)):
          return jsonify({"success": False, "error": "invalid email"})
       if password != conf_password:
            return "password doesn't match"
       if not username:
            return "Missing username"
       query = {"username": username}     
       user_data = db.users.find_one(query)
       if user_data is None: 
            newvalues = {
                        'username': username,
                        'email': email,
                        'password': password,
                }
            db.users.insert_one(newvalues)
            return "signup success"
       else:
            return "Username already exists."
    else:
        return render_template("register.html")

@app.route("/login", methods=['POST'])
def login():
    try:
        if request.method == "POST":          
            username = request.form.get("username")
            password = request.form.get("password")
            query = {"username": username}
            userData = db.users.find_one(query)
            if userData is not None:
                user_password = userData['password']
                if password == user_password:
                    return "login success"
                else:
                    return "Invalid Credentials"
            else:
                return "Invalid User or user doesn't exist."
        else:
            return "Invalid request"
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/properties")
def properties():
    return render_template("properties.html")

@app.route("/add-property")
def add_property():
    return render_template("add-property.html")

@app.route("/agent")
def agent():
    return render_template("agent.html")

@app.route("/agency")
def agency():
    return render_template("agency.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/services")
def services():
    return render_template("services.html")


if __name__ == '__main__':
    app.run(debug=True)