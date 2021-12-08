from datetime import datetime
from flask import Flask, render_template, request, url_for, jsonify, json, send_file, send_from_directory,session
import pymongo
from pymongo.message import query
import requests
import os, sys
import re
from bson.objectid import ObjectId
from os.path import join, dirname, realpath
from werkzeug.utils import redirect, secure_filename
from PIL import Image

app = Flask(__name__)

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "properties"
db = client[database_name]

# USER IMAGES UPLOAD FOLDER
PROPERTIES_FOLDER = join(dirname(realpath(__file__)), 'static/img/property')
PROFILE_FOLDER = join(dirname(realpath(__file__)), 'static/img/profile')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',}
app.config['PROPERTIES_FOLDER'] = PROPERTIES_FOLDER
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def hello_world():
    sale_query = {"status": "sale"} 
    rent_query = {"status": "rent"} 
    featured_query = {"featured": True} 
    new_properties_sale = db.properties.find(sale_query).sort("timestamp", -1)
    new_properties_rent = db.properties.find(rent_query).sort("timestamp", -1)
    featured_properties = db.properties.find(featured_query)
    sale_lists = []
    for i in new_properties_sale:
        i.update({"_id": str(i["_id"])})
        sale_lists.append(i)
    rent_lists = []
    for i in new_properties_rent:
        i.update({"_id": str(i["_id"])})
        rent_lists.append(i)
    featured_lists = []
    for i in featured_properties:
        i.update({"_id": str(i["_id"])})
        featured_lists.append(i)
    if 'loggedin' in session:
        return render_template("index-9.html",sale_new=sale_lists, rent_new=rent_lists,featured=featured_lists,username=session['username'])
    else:
        return render_template("index-9.html",sale_new=sale_lists, rent_new=rent_lists,featured=featured_lists)

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
       fullname = request.form.get("fullname")
       username = request.form.get("username")
       phone = request.form.get("phone")       
       email = request.form.get("email")
       city = request.form.get("city")
       password = request.form.get("password")
       conf_password = request.form.get("conf_password")
       type = request.form.get("type")
       profile_pic = request.files.get('profile_pic')
       if profile_pic:
            if allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(
                    os.path.join(app.config['PROFILE_FOLDER'], filename))
                # compress image
                newimage = Image.open(os.path.join(app.config['PROFILE_FOLDER'], str(filename)))
                newimage.thumbnail((400, 400))
                newimage.save(os.path.join(PROFILE_FOLDER, str(filename)), quality=95)
            else:
                return "picture format is not supported"
       regex = '[^@]+@[a-zA-Z0-9]+[.][a-zA-Z]+'
       if not (re.search(regex, email)):
          return "invalid email"
       if password != conf_password:
            return "password doesn't match"
       if not username:
            return "Missing username"
       query = {"username": username}          
       agent_data = db.agents.find_one(query)
       user_data = db.users.find_one(query)
       if type == 'agent': 
           if agent_data is None and user_data is None:
               newvalues =  {
                        'username': username,
                        'fullname': fullname,
                        'phone': phone,
                        'email': email,
                        'city': city,
                        'password': password,
                        'type':type,
                        'profile_pic':filename
                }
               db.agents.insert_one(newvalues)
               return "registered"
           else:
               return "Agent already exists."
       else:    
            if user_data is None and agent_data is None: 
                newvalues = {
                            'username': username,
                            'fullname': fullname,
                            'phone': phone,
                            'email': email,
                            'city': city,
                            'password': password,
                            'type':type,
                            'profile_pic':filename
                    }
                db.users.insert_one(newvalues)
                return "Registered"
            else:
                return "User already exists."
    else:
        return render_template("register.html")
@app.route("/test2")
def test2():
    return session["type"]

# login from modal 
@app.route("/login", methods=['POST'])
def login():
    try:
        if request.method == "POST":          
            username = request.form.get("username")
            password = request.form.get("password")
            query = {"username": username}
            userData = db.users.find_one(query)
            agentData = db.agents.find_one(query)
            if userData is not None:
                user_password = userData['password']
                if password == user_password:
                    session['loggedin'] = True
                    session['id'] = str(userData['_id'])
                    session['username'] = userData['username']
                    session['type'] = userData['type']
                    return redirect(url_for('hello_world'))
                else:
                    return "Invalid Credentials"
            elif agentData is not None:
                agent_password = agentData['password']
                if password == agent_password:
                    session['loggedin'] = True
                    session['id'] = str(agentData['_id'])
                    session['username'] = agentData['username']
                    session['type'] = agentData['type']
                    return redirect(url_for('hello_world'))
                else:
                    return "Invalid Credentials"
            else:
                return "Invalid User or user doesn't exist."
        else:
            return "Invalid request"
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# login from login template template 
@app.route("/login2", methods=['GET','POST'])
def login2():
    try:
        if request.method == "POST":          
            username = request.form.get("username")
            password = request.form.get("password")
            query = {"username": username}
            userData = db.users.find_one(query)
            agentData = db.agents.find_one(query)
            if userData is not None:
                user_password = userData['password']
                if password == user_password:
                    session['loggedin'] = True
                    session['id'] = str(userData['_id'])
                    session['username'] = userData['username']
                    session['type'] = userData['type']

                    return redirect(url_for('hello_world'))
                else:
                    return "Invalid Credentials"
            elif agentData is not None:
                agent_password = agentData['password']
                if password == agent_password:
                    session['loggedin'] = True
                    session['id'] = str(agentData['_id'])
                    session['username'] = agentData['username']
                    session['type'] = agentData['type']
                    return redirect(url_for('hello_world'))
                else:
                    return "Invalid Credentials"
            else:
                return "Invalid User or user doesn't exist."
        else:
            return render_template("login.html")
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# configure logout route
@app.route('/logout')
def logout():
        # Remove session data, this will log the user out 
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        # Redirect to index page
        return redirect(url_for('hello_world'))


@app.route("/about-us")
def about_us():
    if 'loggedin' in session:
        return render_template("about-us.html",username=session['username'])
    else:
        return render_template("about-us.html")

# @app.route("/blog")
# def blog():
#     return render_template("blog.html")

@app.route("/properties")
def properties():
    properties = db.properties.find()
    # return str(properties)
    lists = []
    # for loop
    for i in properties:
        i.update({"_id": str(i["_id"])})
        lists.append(i)
    if 'loggedin' in session:
        return render_template("properties.html", properties=lists,username=session['username'])
    else:
        return render_template("properties.html", properties=lists)

@app.route("/find-your-dream-home", methods=['GET','POST'])
def find_your_dream_home():
    try:
        city = None    
        typee = None
        status = None
        bedroom = None
        bathroom = None
        kitchen = None
        min_area = None
        max_area = None
        floor = None
        price = None
        if request.form.get("city"):
            city = request.form.get("city")
        if request.form.get("type"):
            typee = request.form.get("type")
        if request.form.get("status"):
            status = request.form.get("status")
        if request.form.get("bedroom"):
            bedroom = request.form.get("bedroom")
        if request.form.get("bathroom"):
            bathroom = request.form.get("bathroom")
        if request.form.get("kitchen"):
            kitchen = request.form.get("kitchen")
        if request.form.get("min_area"):
            min_area = request.form.get("min_area")
        if request.form.get("max_area"):
            max_area = request.form.get("max_area")
        if request.form.get("floor"):
            floor = request.form.get("floor")
        if request.form.get("price"):
            price = request.form.get("price")
        # concat price
        numbers = re.findall('\d+', price)
        min_price = int(numbers[0])
        max_price = int(numbers[1])

        # if everything is given 
        if city != None and typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city, "type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}

        # if everything is given except city
        elif typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except type
        elif city != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except status
        elif city != None and typee != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city,"type":typee,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except bedroom
        elif city != None and typee != None and status != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city,"type":typee,"status":status,"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except bathroom
        elif city != None and typee != None and status != None and bedroom != None and kitchen != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city,"type":typee,"status":status,"bedroom":int(bedroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except kitchen
        elif city != None and typee != None and status != None and bedroom != None and bathroom != None and min_area != None and max_area != None and floor != None and price != None: 
            query = {"city":city,"type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except min_area and max_area
        elif city != None and typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and floor != None and price != None: 
            query = {"city":city,"type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"floor":floor,"kitchen":int(kitchen),"price":{"$gt":min_price,"$lt":max_price}}

        # if only city is given
        elif city != None: 
            query = {"city":city}
        # if only type is given
        elif typee != None: 
            query = {"type":typee}
        # if only status is given
        elif status != None: 
            query = {"status":status}
        # if only floor is given
        elif floor != None: 
            query = {"floor":floor}
        # if only min-max area are given
        elif min_area != None and max_area != None: 
            query = {"area":{"$gt":int(min_area),"$lt":int(max_area)}}

        # if only city and type are given 
        elif city != None and typee != None: 
            query = {"city":city,"type":typee}
        # if only city and status are given 
        elif city != None and status != None: 
            query = {"city":city,"status":status}
        # if only city and floor are given 
        elif city != None and floor != None: 
            query = {"city":city,"floor":floor}

        # if only city and type and status are given 
        elif city != None and typee != None and status != None: 
            query = {"city":city,"type":typee,"status":status}

        # if only city and type and status and floor are given 
        elif city != None and typee != None and status != None and floor != None: 
            query = {"city":city,"type":typee,"status":status,"floor":floor}

        # if only city and type and status and floor and area are given 
        elif city != None and typee != None and status != None and floor != None and min_area != None and max_area != None: 
            query = {"city":city,"type":typee,"status":status,"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)}}

        # if nothing is given 
        elif city == None and typee == None and status == None and bedroom == None and bathroom == None and kitchen == None and min_area == None and max_area == None and floor == None:
            query={"price":{"$gt":min_price,"$lt":max_price}}
        
        # result = db.properties.find()
        result = db.properties.find(query)
        results = []
        # for loop
        for i in result:
            i.update({"_id": str(i["_id"]),})
            results.append(i)
        
        if 'loggedin' in session:
            return render_template("find_your_dream_home.html",properties=results,username=session['username'])
        else:
            return render_template("find_your_dream_home.html",properties=results)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
        
@app.route("/single-properties/<propertyid>")
def single_properties(propertyid):
    query = {"_id": ObjectId(propertyid)} 
    property = db.properties.find_one(query)    
    pictures = property["pictures"]
    query = {"property_id": ObjectId(propertyid)} 
    feedbacks = db.reviews.find(query)
    reviews = []
    # for loop
    for i in feedbacks:
        i.update({"_id": str(i["_id"]),"property_id":str(i["property_id"])})
        reviews.append(i)
    total_reviews = len(reviews)

    if 'loggedin' in session:
        return render_template("single-properties.html", property=property,pics=pictures,reviews=reviews,total_reviews=total_reviews,username=session['username'])
    else:
        return render_template("single-properties.html", property=property,pics=pictures,reviews=reviews,total_reviews=total_reviews)

@app.route("/add-property", methods=['GET','POST'])
def add_property():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form.get("title")
            price = request.form.get("price")
            desc = request.form.get("desc")
            city = request.form.get("city")
            address = request.form.get("address")
            type = request.form.get("type")
            floor = request.form.get("floor")
            status = request.form.get("status")
            bedroom = request.form.get("bedroom")
            bathroom = request.form.get("bathroom")
            kitchen = request.form.get("kitchen")
            area = request.form.get("area")
            balcony = False
            parking = False
            lift = False
            pool = False
            timestamp = datetime.now()
            if request.form.get("balcony") == "on":
                balcony = True
            if request.form.get("parking") == "on":
                parking = True
            if request.form.get("lift") == "on":
                lift = True
            if request.form.get("pool") == "on":
                pool = True

            # save pictures
            pictures = request.files.getlist("pictures")
            filenames = []
            for picture in pictures:
                if picture and allowed_file(picture.filename):
                    filename = secure_filename(picture.filename)
                    print (filename)
                    picture.save(
                        os.path.join(app.config['PROPERTIES_FOLDER'], filename))
                    filename=filenames.append(filename)  
                else:
                    return "picture not found or incorrect format"
            # save display picture
            display_picture = request.files.get("display_pic")
            if display_picture and allowed_file(display_picture.filename):
                filename = secure_filename(display_picture.filename)
                print (filename)
                display_picture.save(
                    os.path.join(app.config['PROPERTIES_FOLDER'], filename))  
            else:
                return "picture not found or incorrect format"
            newProperty={
                "title":title,
                "price":float(price),
                "desc":desc,
                "city":city,
                "address":address,
                "type":type,
                "floor":floor,
                "status":status,
                "bedroom":int(bedroom),
                "bathroom":int(bathroom),
                "kitchen":int(kitchen),
                "area":int(area),
                "balcony":balcony, 
                "parking":parking, 
                "lift":lift,
                "pool":pool,
                "timestamp":timestamp,
                "pictures":filenames,
                "display_pic":filename
            }
            db.properties.insert_one(newProperty)
            return "True"
        else:
            return render_template("add-property.html",username= session['username'])
    else:
        return redirect(url_for('login2'))


@app.route("/agent")
def agent():
    return render_template("agent.html")

@app.route("/agency")
def agency():
    return render_template("agency.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/save-review/<propertyid>", methods=['POST'])
def save_review(propertyid):
    if request.method == 'POST':
        feedback = request.form.get("review")
        name = session['username']
        time = datetime.now()        
        id = session['id']
        query = {"_id":ObjectId(id)}
        userAccount = db.users.find_one(query)
        agentAccount = db.users.find_one(query)
        if userAccount is not None:
            newvalues = {
                "property_id":ObjectId(propertyid),
                "name":name,
                "feedback":feedback,
                "time":time,
                "profile_pic":userAccount['profile_pic']
            }
            db.reviews.insert_one(newvalues)
            return redirect("/single-properties/"+ propertyid)
        elif agentAccount is not None:
            newvalues = {
                "property_id":ObjectId(propertyid),
                "name":name,
                "feedback":feedback,
                "time":time,
                "profile_pic":agentAccount['profile_pic']
            }
            db.reviews.insert_one(newvalues)
            return redirect("/single-properties/"+ propertyid)
    else: 
        return "Invalid method"

@app.route("/contact-form", methods=['GET','POST'])
def contact_form():
    if request.method == 'POST':
        if "loggedin" in session:
            msg = request.form.get("msg")            
            if not msg:
                return "Please fill all required fields"
            query = {"_id":ObjectId(session['id'])}
            userData = db.users.find_one(query)
            newData = {
                "name": userData['fullname'],
                "email": userData['email'],
                "type": userData['type'],
                "msg": msg,
            }
            db.contact.insert_one(newData)
            return "Message Sent Successfully"
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            msg = request.form.get('msg')
            if not name or not email or not msg:
                return "Please fill all required fields"
            regex = '[^@]+@[a-zA-Z0-9]+[.][a-zA-Z]+'
            if not (re.search(regex, email)):
                return str("invalid email")
            else:                
                newData = {
                    "name":name,
                    "email":email,
                    "type":"unknown",
                    "msg":msg
                }
                db.contact.insert_one(newData)
                return "Message Sent Successfully"
    else:
        if "loggedin" in session:
            return render_template("contact.html",username = session['username'])
        else:
            return render_template("contact.html")
        
@app.route("/myaccount/<username>")
def myaccount(username):
    if request.method == "POST":
        re
    else:
        query = {"username":username}
        userAccount=db.users.find_one(query)
        agentAccount=db.agents.find_one(query)
        if userAccount is not None: 
            account = userAccount
            return render_template("my-account.html", username = session['username'], account=account)
        elif agentAccount is not None: 
            account = agentAccount           
            return render_template("my-account.html", username = session['username'], account=account)
        else:
            return "invalid username"
        
@app.route("/edit-account/<id>", methods=['POST'])
def editaccount(id):
    if request.method == "POST":
        # first check wheather account type is agent or normal user 
        query = {"_id": ObjectId(id)}
        userAccount = db.users.find_one(query)
        agentAccount = db.agents.find_one(query)
        # if account type is user 
        if userAccount is not None:
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")         
            facebook = request.form.get("facebook")
            instagram = request.form.get("instagram")
            website = request.form.get("website")
            profile_pic = request.files.get('profile_pic')            
            if profile_pic:
                if allowed_file(profile_pic.filename):
                    filename = secure_filename(profile_pic.filename)
                    profile_pic.save(
                        os.path.join(app.config['PROFILE_FOLDER'], filename))
                    # compress image
                    newimage = Image.open(os.path.join(app.config['PROFILE_FOLDER'], str(filename)))
                    newimage.thumbnail((400, 400))
                    newimage.save(os.path.join(PROFILE_FOLDER, str(filename)), quality=95)
                else:
                    return "picture format is not supported"
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'profile_pic': filename,
                        'fullname':name,
                        'email':email,
                        'phone':phone
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.users.update_one(filter, newvalues)
                return redirect("/myaccount/"+userAccount['username'])
            else:
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'fullname':name,
                        'email':email,
                        'phone':phone
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.users.update_one(filter, newvalues)
                return redirect("/myaccount/"+userAccount['username'])
        elif agentAccount is not None:
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")   
            facebook = request.form.get("facebook")
            instagram = request.form.get("instagram")
            website = request.form.get("website")
            profile_pic = request.files.get('profile_pic')
            
            if profile_pic:
                if allowed_file(profile_pic.filename):
                    filename = secure_filename(profile_pic.filename)
                    profile_pic.save(
                        os.path.join(app.config['PROFILE_FOLDER'], filename))
                    # compress image
                    newimage = Image.open(os.path.join(app.config['PROFILE_FOLDER'], str(filename)))
                    newimage.thumbnail((400, 400))
                    newimage.save(os.path.join(PROFILE_FOLDER, str(filename)), quality=95)
                else:
                    return "picture format is not supported"
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'profile_pic': filename,
                        'fullname':name,
                        'email':email,
                        'phone':phone
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.agents.update_one(filter, newvalues)            
                return redirect("/myaccount/"+agentAccount['username'])
            else:
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'fullname':name,
                        'email':email,
                        'phone':phone
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.agents.update_one(filter, newvalues)            
                return redirect("/myaccount/"+agentAccount['username'])


@app.route("/change-password/<id>", methods=['POST'])
def changepassword(id):
    if request.method == 'POST':
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        last_password_change = datetime.now()
        query = {"_id":ObjectId(id)}
        userAccount = db.users.find_one(query)
        agentAccount = db.agents.find_one(query)
        if userAccount is not None:
            if old_password == userAccount['password']:
                if new_password == confirm_password:
                    newvalues = {
                        '$set':{
                            "password":new_password,
                            "last_password_change":last_password_change
                        }
                    }
                    filter = {'_id': ObjectId(id)}
                    db.users.update_one(filter,newvalues)
                    return redirect("/myaccount/"+userAccount['username'])
                else:
                    "passwords don't matched"
            else:
                return "Invalid old password"
        elif agentAccount is not None:
            if old_password == agentAccount['password']:
                if new_password == confirm_password:
                    newvalues = {
                        '$set':{
                            "password":new_password,
                            "last_password_change":last_password_change
                        }
                    }
                    filter = {'_id': ObjectId(id)}
                    db.agents.update_one(filter,newvalues)
                    return redirect("/myaccount/"+agentAccount['username'])
                else:
                    "passwords don't matched"
            else:
                return "Invalid old password"
        else:
            return "invalid userid"
    else:
        return "Invalid request"

@app.route("/delete-account/<id>", methods=['GET','POST'])
def deletepassword(id):
    if request.method == 'POST':
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            return "password didn't match"
        query = {"_id":ObjectId(id)}
        userAccount = db.users.find_one(query)
        agentAccount = db.agents.find_one(query)
        if userAccount is not None:
            if password == userAccount['password']:
                db.users.delete_one(query)
                return redirect(url_for('logout'))
            else:
                return "Incorrect Password"
        elif agentAccount is not None:
            if password == agentAccount['password']:
                db.agents.delete_one(query)
                return redirect(url_for('logout'))
            else:
                return "Incorrect Password"
    else:
        return render_template("delete-account.html",username = session['username'],id=id)




if __name__ == '__main__':
    app.run(debug=True)