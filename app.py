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
from flask_mail import Mail, Message
import 

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

app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.ionos.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'property@globalcaregroup.net'
app.config['MAIL_PASSWORD'] = '@kwebtrica321'
app.config['MAIL_DEFAULT_SENDER'] = ('property@globalcaregroup.net', "property@globalcaregroup.net")
mail = Mail(app)

# test-mail 
@app.route("/send")
def send():
    msg = Message("HELLO THIS IS FOR TESTING", recipients=["mali29april@gmail.com"])
    mail.send(msg)
    return "True"


# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def hello_world():
    sale_query = {"status": "sale","sold":{"$ne":True}} 
    rent_query = {"status": "rent","sold":{"$ne":True}} 
    featured_query = {"featured": True,"sold":{"$ne":True}} 
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
    # fetch agents 
    agents = db.agents.find()
    agentLists = []
    for i in agents:
        i.update({"_id":str(i["_id"])})
        agentLists.append(i)
    if 'loggedin' in session:
        if session['type'] != 'admin':
            return render_template("index-9.html",sale_new=sale_lists, rent_new=rent_lists,featured=featured_lists,username=session['username'],agents=agentLists)
        else:
            return render_template("index-9.html",sale_new=sale_lists, rent_new=rent_lists,featured=featured_lists,agents=agentLists)
    else:
        return render_template("index-9.html",sale_new=sale_lists, rent_new=rent_lists,featured=featured_lists,agents=agentLists)

@app.route("/register", methods=['GET','POST'])
def register():
    msg = ''
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
        regex = '[^@]+@[a-zA-Z0-9]+[.][a-zA-Z]+'
        if not (re.search(regex, email)):
            msg = "invalid email"
            return render_template("register.html" ,msg=msg)
        if password != conf_password:
                msg =  "password doesn't match"
                return render_template("register.html" ,msg=msg)
        if not username:
                msg = "Missing username"
                return render_template("register.html" ,msg=msg)
        
        if profile_pic.filename:
            if profile_pic and allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(
                    os.path.join(app.config['PROFILE_FOLDER'], filename))
                # compress image
                newimage = Image.open(os.path.join(app.config['PROFILE_FOLDER'], str(filename)))
                newimage.thumbnail((400, 400))
                newimage.save(os.path.join(PROFILE_FOLDER, str(filename)), quality=95)
            else:
                msg = "Profile picture not found or format is not supported"
                return render_template("register.html" ,msg=msg)
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
                    msg = "You are registered!"
                    return render_template("login.html",success_msg=msg)
                else:
                    msg = "Agent already exists."
                    return render_template("register.html" ,msg=msg)
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
                        msg = "You are registered!"
                        return render_template("login.html",success_msg=msg)
                    else:
                        msg = "User already exists."
                        return render_template("register.html" ,msg=msg)
        else:            
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
                                'profile_pic':"default.jpg"
                        }
                    db.agents.insert_one(newvalues)
                    msg = "You are registered!"
                    return render_template("login.html",success_msg=msg)
                else:
                    msg = "Agent already exists."
                    return render_template("register.html" ,msg=msg)
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
                                    'profile_pic':"default.jpg"
                            }
                        db.users.insert_one(newvalues)
                        msg = "You are registered!"
                        return render_template("login.html",success_msg=msg)
                    else:
                        msg = "User already exists."
                        return render_template("register.html" ,msg=msg)
            
    else:
        return render_template("register.html")

# login from modal 
@app.route("/login", methods=['POST'])
def login():
    msg = ''
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
                    msg = "Invalid Password"
                    return render_template("index-9.html",msg=msg)
            elif agentData is not None:
                agent_password = agentData['password']
                if password == agent_password:
                    session['loggedin'] = True
                    session['id'] = str(agentData['_id'])
                    session['username'] = agentData['username']
                    session['type'] = agentData['type']
                    return redirect(url_for('hello_world'))
                else:
                    msg = "Invalid Password"
            else:
                msg = "Invalid User or user doesn't exist."
        else:
            return "Invalid request"
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# login from login template template 
@app.route("/login2", methods=['GET','POST'])
def login2():
    msg = ''
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
                msg = "Invalid Password"
                return render_template("login.html",msg=msg)
        elif agentData is not None:
            agent_password = agentData['password']
            if password == agent_password:
                session['loggedin'] = True
                session['id'] = str(agentData['_id'])
                session['username'] = agentData['username']
                session['type'] = agentData['type']
                return redirect(url_for('hello_world'))
            else:
                msg = "Invalid Password"
                return render_template("login.html",msg=msg)
        else:
            msg = "Invalid User or user doesn't exist."
            return render_template("login.html",msg=msg)
    else:
        return render_template("login.html")

# configure logout route
@app.route('/logout')
def logout():
        # Remove session data, this will log the user out 
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('type', None)
        # Redirect to index page
        return redirect(url_for('hello_world'))


@app.route("/about-us")
def about_us():
    if 'loggedin' in session:
        if session['type'] != 'admin':
            return render_template("about-us.html",username=session['username'])
        else:            
            return render_template("about-us.html")
    else:
        return render_template("about-us.html")

@app.route("/properties")
def properties():
    query ={"sold":{"$ne":True}}
    properties = db.properties.find(query)
    # return str(properties)
    lists = []
    # for loop
    for i in properties:
        query = {"property_id":i["_id"]}
        viewsData = db.property_views.find(query)
        viewsLists = []
        for view in viewsData:
            view.update({"_id": str(view["_id"])})
            viewsLists.append(view)
        total_views = len(viewsLists)       

        i.update({"_id": str(i["_id"]),"total_views":total_views})
        lists.append(i)

    if 'loggedin' in session:
        if session['type'] != 'admin':
            return render_template("properties.html", properties=lists,username=session['username'])
        else:
            return render_template("properties.html", properties=lists)
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
        min_price = None
        max_price = None
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
        if request.form.get("min_price"):
            min_price = request.form.get("min_price")
        if request.form.get("max_price"):
            max_price = request.form.get("max_price")
        # concat price)
        # numbers = re.findall('\d+', price)
        # min_price = int(numbers[0])
        # max_price = int(numbers[1])

        # if everything is given 
        if city != None and typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city, "type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":int(min_price),"$lt":int(max_price)}}

        # if everything is given except city
        elif typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except type
        elif city != None and status != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except status
        elif city != None and typee != None and bedroom != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city,"type":typee,"bedroom":int(bedroom),"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except bedroom
        elif city != None and typee != None and status != None and bathroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city,"type":typee,"status":status,"bathroom":int(bathroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except bathroom
        elif city != None and typee != None and status != None and bedroom != None and kitchen != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city,"type":typee,"status":status,"bedroom":int(bedroom),"kitchen":int(kitchen),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except kitchen
        elif city != None and typee != None and status != None and bedroom != None and bathroom != None and min_area != None and max_area != None and floor != None and min_price != None and max_price != None: 
            query = {"city":city,"type":typee,"status":status,"bedroom":int(bedroom),"bathroom":int(bathroom),"floor":floor,"area":{"$gt":int(min_area),"$lt":int(max_area)},"price":{"$gt":min_price,"$lt":max_price}}
        # if everything is given except min_area and max_area
        elif city != None and typee != None and status != None and bedroom != None and bathroom != None and kitchen != None and floor != None and min_price != None and max_price != None: 
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
        elif city == None and typee == None and status == None and bedroom == None and bathroom == None and kitchen == None and min_area == None and max_area == None and floor == None and min_price == None and max_price == None:
            query={}
        # if only prices are given 
        elif city == None and typee == None and status == None and bedroom == None and bathroom == None and kitchen == None and min_area == None and max_area == None and floor == None and min_price != None and max_price != None:
            query={"price":{"$gt":int(min_price),"$lt":int(max_price)}}
        
        # result = db.properties.find()
        result = db.properties.find(query)
        results = []
        # for loop
        for i in result:
            i.update({"_id": str(i["_id"]),})
            results.append(i)
        
        if 'loggedin' in session:
            if session['type'] != 'admin':
                return render_template("find_your_dream_home.html",properties=results,username=session['username'])
            else:
                return render_template("find_your_dream_home.html",properties=results)
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

    # now increase one view     
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    query = {"ip_address":ip_address,"property_id":ObjectId(propertyid)}
    viewexist = db.property_views.find_one(query)
    if viewexist is None:
        newValues = {
            "property_id":ObjectId(propertyid),
            "ip_address":ip_address,
            "timestamp":datetime.now()
        }
        db.property_views.insert_one(newValues)
    # .... 
    # fetch 4 latest featured properties for sidebar 
    query = {"featured":True,"sold":{"$ne":True}}
    featured_properties = db.properties.find(query).limit(4)
    f_prop_lists = []
    for prop in featured_properties:
        prop.update({"_id": str(prop["_id"])})
        f_prop_lists.append(prop)
    # ......     
    # fetch 6 latest agents for sidebar
    our_agents = db.agents.find().limit(6)
    agents_lists = []
    for agent in our_agents:
        agent.update({"_id": str(agent["_id"])})
        agents_lists.append(agent)
    # ......     

    if 'loggedin' in session:
        if session['type'] != 'admin':
            return render_template("single-properties.html", property=property,pics=pictures,reviews=reviews,total_reviews=total_reviews,username=session['username'],featured=f_prop_lists,agents=agents_lists)
        else:
            return render_template("single-properties.html", property=property,pics=pictures,reviews=reviews,total_reviews=total_reviews,featured=f_prop_lists,agents=agents_lists)
    else:
        return render_template("single-properties.html", property=property,pics=pictures,reviews=reviews,total_reviews=total_reviews,featured=f_prop_lists,agents=agents_lists)

@app.route("/add-property", methods=['GET','POST'])
def add_property():
    if 'loggedin' in session:
        if session['type'] != 'admin':
            msg = ''
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
                # return str(request.files.getlist("images[]"))
                # return str(request.files.getlist("pictures"))

                # save pictures
                # pictures = request.files.getlist("pictures")
                pictures = request.files.getlist("images[]")
                filenames = []
                for picture in pictures:
                    if picture and allowed_file(picture.filename):
                        filename = secure_filename(picture.filename)
                        # print (filename)
                        picture.save(
                            os.path.join(PROPERTIES_FOLDER, filename))
                        filename=filenames.append(filename)                 
                        # compress image and set dimensions
                        # newimage = Image.open(os.path.join(PROPERTIES_FOLDER, str(filename)))
                        # newimage.resize((368, 287))
                        # newimage.save(os.path.join(PROPERTIES_FOLDER, str(filename)), quality=95) 
                    else:
                        msg = "picture not found or incorrect format"
                        return render_template("add-property.html",username = session['username'],msg=msg)
                # fetch the last item from the list that is display_pic 
                display_pic = filenames[-1] 
                # delete the last item from the list 
                del filenames[-1]
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
                    "display_pic":display_pic,
                    "added-by":session['id'],
                    # byDefault 
                    "featured":False,
                }
                db.properties.insert_one(newProperty)
                query = {"title":title,"desc":desc,"timestamp":timestamp}
                addedpropery = db.properties.find_one(query)
                propertyid = str(addedpropery['_id'])
                return redirect("/single-properties/"+ propertyid)
            else:
                return render_template("add-property.html",username= session['username'])
        else:
            return redirect(url_for('login2'))
    else:
        return redirect(url_for('login2'))


@app.route("/agent")
def agent():
    agents = db.agents.find()
    lists = []
    # for loop
    for i in agents:
        i.update({"_id": str(i["_id"])})
        lists.append(i)
    if "loggedin" in session:
        return render_template("agent.html",username=session['username'],agents=lists)
    else:
        return render_template("agent.html",agents=lists)

@app.route("/agent-details/<id>")
def agent_details(id):
    query = {"_id":ObjectId(id)}
    agent = db.agents.find_one(query)
    query = {"agentid":ObjectId(id)}

    # for totalviews of agents. 
    viewsData = db.agent_contact_number_views.find(query)    
    views_lists = []
    for i in viewsData:
        i.update({"_id": str(i["_id"])})
        views_lists.append(i)
    totalviews = len(views_lists)
    # ...

    if "loggedin" in session:
        return render_template("agent-details.html",username=session['username'],agent=agent,views=totalviews)
    else:
        return render_template("agent-details.html",agent=agent,views=totalviews)

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
            if session['type'] != 'admin' and session['type'] != 'agent':
                mesg = request.form.get("msg")            
                if not mesg:
                    return "Please fill all required fields"
                query = {"_id":ObjectId(session['id'])}
                userData = db.users.find_one(query)
                newData = {
                    "name": userData['fullname'],
                    "email": userData['email'],
                    "type": userData['type'],
                    "msg": mesg,
                }
                db.contact.insert_one(newData)                
                msg = Message("Properties! New Message", recipients=["property@globalcaregroup.net"])
                msg.html = str("<p>Name:&nbsp;"+str(userData['fullname'])+"</p><p>Email:&nbsp;"+str(userData['email'])+"</p><p> type:&nbsp;"+str(userData['type'])+"</p><p> msg:&nbsp; "+str(mesg)+"</p>")
                mail.send(msg)
                msg = Message("Properties!", recipients=[str(userData['email'])])
                msg.html = str("<p>Dear,"+str(userData['fullname'])+"</p><p>We have received your email, and our support team will be in touch with you soon.</p><p>Best regards,</p><p>Properties</p>")
                mail.send(msg)
                return "Message Sent Successfully"
            elif session['type'] == 'agent':
                mesg = request.form.get("msg")            
                if not mesg:
                    return "Please fill all required fields"
                query = {"_id":ObjectId(session['id'])}
                agentData = db.agents.find_one(query)
                newData = {
                    "name": agentData['fullname'],
                    "email": agentData['email'],
                    "type": agentData['type'],
                    "msg": mesg,
                }
                db.contact.insert_one(newData)
                msg = Message("Properties! New Message", recipients=["property@globalcaregroup.net"])
                msg.html = str("<p>Name:&nbsp;"+str(agentData['fullname'])+"</p><p>Email:&nbsp;"+str(agentData['email'])+"</p><p> type:&nbsp;"+str(agentData['type'])+"</p><p> msg:&nbsp; "+str(mesg)+"</p>")
                mail.send(msg)
                msg = Message("Properties!", recipients=[str(agentData['email'])])
                msg.html = str("<p>Dear,"+str(agentData['fullname'])+"</p><p>We have received your email, and our support team will be in touch with you soon.</p><p>Best regards,</p><p>Properties</p>")
                mail.send(msg)
                return "Message Sent Successfully"
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            mesg = request.form.get('msg')
            if not name or not email or not mesg:
                return "Please fill all required fields"
            regex = '[^@]+@[a-zA-Z0-9]+[.][a-zA-Z]+'
            if not (re.search(regex, email)):
                return str("invalid email")
            else:                
                newData = {
                    "name":name,
                    "email":email,
                    "type":"unknown",
                    "msg":mesg
                }
                db.contact.insert_one(newData)
                msg = Message("Properties! New Message", recipients=["property@globalcaregroup.net"])
                msg.html = str("<p>Name:&nbsp;"+str(name)+"</p><p>Email:&nbsp;"+str(email)+"</p><p> type:&nbsp;"+"unknown"+"</p><p> msg:&nbsp; "+str(mesg)+"</p>")
                mail.send(msg)
                msg = Message("Properties!", recipients=[str(email)])
                msg.html = str("<p>Dear,"+str(name)+"</p><p>We have received your email, and our support team will be in touch with you soon.</p><p>Best regards,</p><p>Properties</p>")
                mail.send(msg)
                return "Message Sent Successfully"
    else:
        if "loggedin" in session:
            return render_template("contact.html",username = session['username'])
        else:
            return render_template("contact.html")
        
@app.route("/myaccount/<username>/<msg>")
def myaccount(username,msg):
    try:
        query = {"username":username}
        userAccount=db.users.find_one(query)
        agentAccount=db.agents.find_one(query)
        if userAccount is not None: 
            account = userAccount
            return render_template("my-account.html", username = session['username'], account=account,msg=msg)
        elif agentAccount is not None: 
            account = agentAccount           
            return render_template("my-account.html", username = session['username'], account=account,msg=msg)
        else:
            return "invalid username"
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
        
@app.route("/edit-account/<id>", methods=['POST'])
def editaccount(id):
    msg = ''
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
                    msg = "picture format is not supported"                    
                    return redirect("/myaccount/"+userAccount['username']+"/"+str(msg))
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'profile_pic': filename,
                        'fullname':name,
                        'email':email,
                        'phone':phone,
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.users.update_one(filter, newvalues)
                return redirect("/myaccount/"+userAccount['username']+"/msg")
            else:
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'fullname':name,
                        'email':email,
                        'phone':phone,
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.users.update_one(filter, newvalues)
                return redirect("/myaccount/"+userAccount['username']+"/msg")
        elif agentAccount is not None:
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")   
            facebook = request.form.get("facebook")
            instagram = request.form.get("instagram")
            website = request.form.get("website")
            profile_pic = request.files.get('profile_pic')
            about = request.form.get("about")
            biography = request.form.get("biography")
            completed_projects = request.form.get("completed_projects")
            property_sold = request.form.get("property_sold")
            happy_clients = request.form.get("happy_clients")
            experience = request.form.get("experience")
            
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
                    msg = "picture format is not supported"                                        
                    return redirect("/myaccount/"+agentAccount['username']+"/"+msg)
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'profile_pic': filename,
                        'fullname':name,
                        'email':email,
                        'phone':phone,
                        'about':about,
                        'biography':biography,
                        'completed_projects':int(completed_projects),
                        'property_sold':int(property_sold),
                        'happy_clients':int(happy_clients),
                        'working_experience':experience
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.agents.update_one(filter, newvalues)            
                return redirect("/myaccount/"+agentAccount['username']+"/msg")
            else:
                newvalues = {
                    "$set": {
                        'facebook': facebook,
                        'instagram': instagram,
                        'website': website,
                        'fullname':name,
                        'email':email,
                        'phone':phone,
                        'about':about,
                        'biography':biography,
                        'completed_projects':int(completed_projects),
                        'property_sold':int(property_sold),
                        'happy_clients':int(happy_clients),
                        'working_experience':experience
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.agents.update_one(filter, newvalues)            
                return redirect("/myaccount/"+agentAccount['username']+"/msg")


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
                    return redirect("/myaccount/"+userAccount['username']+"/msg")
                else:
                    msg = "Passwords don't matched"                                                           
                    return redirect("/myaccount/"+userAccount['username']+"/"+msg)
            else:
                msg = "Invalid Old Password"                                        
                return redirect("/myaccount/"+userAccount['username']+"/"+msg)

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
                    return redirect("/myaccount/"+agentAccount['username']+"/msg")
                else:
                    msg = "Passwords don't matched"                                        
                    return redirect("/myaccount/"+agentAccount['username']+"/"+msg)
            else:
                msg = "Invalid Old Password"                                        
                return redirect("/myaccount/"+agentAccount['username']+"/"+msg)
        else:
            return "Invalid Userid"
    else:
        return "Invalid request"

@app.route("/delete-account/<id>", methods=['GET','POST'])
def deletepassword(id):
    msg = ''
    if request.method == 'POST':
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            msg = "password didn't match"
            return render_template("delete-account.html",username = session['username'],id=id,msg=msg)
        query = {"_id":ObjectId(id)}
        userAccount = db.users.find_one(query)
        agentAccount = db.agents.find_one(query)
        if userAccount is not None:
            if password == userAccount['password']:
                db.users.delete_one(query)
                return redirect(url_for('logout'))
            else:
                msg = "Incorrect Password"
                return render_template("delete-account.html",username = session['username'],id=id,msg=msg)
        elif agentAccount is not None:
            if password == agentAccount['password']:
                db.agents.delete_one(query)
                return redirect(url_for('logout'))
            else:
                msg = "Incorrect Password"
                return render_template("delete-account.html",username = session['username'],id=id,msg=msg)
    else:
        return render_template("delete-account.html",username = session['username'],id=id)

@app.route("/contact-number-viewed",methods=['POST'])
def contact_number_viewed():
    if request.method == 'POST': 
        agentid = request.form.get('agentid')
        agentid = ObjectId(agentid)
        agentusername = request.form.get('agentusername')
        agentfullname = request.form.get('agentfullname')
        username = request.form.get('username')
        print(str(agentid))
        print(str(agentusername))
        print(str(agentfullname))
        print(str(username))
        timestamp = datetime.now()
        query = {"username":username}
        usersData = db.users.find_one(query)
        agentsData = db.agents.find_one(query)
        if usersData is not None:
            userid = usersData['_id']
            userid = ObjectId(userid)
            fullname = usersData['fullname']
            typee = usersData['type']
        elif agentsData is not None:
            userid = agentsData['_id']
            userid = ObjectId(userid)
            fullname = agentsData['fullname']
            typee = agentsData['type']
        elif usersData is None and agentsData is None:
            newValues = {
            "agentid":agentid,
            "agent_username":agentusername,
            "agent_fullname": agentfullname,
            "viewer_type":"unknown",
            "timestamp":timestamp,
            }
            db.agent_contact_number_views.insert_one(newValues)
            return "True"


        newValues = {
            "agentid":agentid,
            "agent_username":agentusername,
            "agent_fullname": agentfullname,
            "viewerid": userid,
            "viewer_fullname":fullname,
            "viewer_type":typee,
            "timestamp":timestamp,
        }
        db.agent_contact_number_views.insert_one(newValues)
        return jsonify({"success":True})

    else:
        return "Invalid request method zam"
    
@app.route("/header-search", methods=['POST'])
def header_search():
    try:
        if request.method == "POST":
            text = request.form.get("text")
            query= {"title":{'$regex': text, '$options' : 'i'}}
            results = db.properties.find(query)
            results_lists = []
            for result in results:                
                result.update({"_id": str(result["_id"])})
                results_lists.append(result)
            
            if "loggedin" in session:
                return render_template("header-search-results.html",properties=results_lists,username=session['username'])
            else:
                return render_template("header-search-results.html",properties=results_lists)

        else:
            return "Invalid request method"
    except Exception as e:        
        return jsonify({"success": False, "error": str(e)})

@app.route("/my-properties/<username>")
def my_properties(username):    
    if 'loggedin' in session:
        if session['type'] != 'admin':
            query = {"username":username}
            agentData = db.agents.find_one(query) 
            userData = db.users.find_one(query)
            if userData: 
                query = {"added-by":str(userData['_id']),"sold":{"$ne":True}}

                properties = db.properties.find(query)
                lists = []
                # for loop
                for i in properties:
                    query = {"property_id":i["_id"]}
                    viewsData = db.property_views.find(query)
                    viewsLists = []
                    for view in viewsData:
                        view.update({"_id": str(view["_id"])})
                        viewsLists.append(view)
                    total_views = len(viewsLists)       

                    i.update({"_id": str(i["_id"]),"total_views":total_views})
                    lists.append(i)

                return render_template("my-properties.html", properties=lists,username=session['username'])                
            elif agentData: 
                query = {"added-by":str(agentData['_id']),"sold":{"$ne":True}}
                properties = db.properties.find(query)
                lists = []
                # for loop
                for i in properties:
                    query = {"property_id":i["_id"]}
                    viewsData = db.property_views.find(query)
                    viewsLists = []
                    for view in viewsData:
                        view.update({"_id": str(view["_id"])})
                        viewsLists.append(view)
                    total_views = len(viewsLists)       

                    i.update({"_id": str(i["_id"]),"total_views":total_views})
                    lists.append(i)

                return render_template("my-properties.html", properties=lists,username=session['username'])
        
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/edit-property-for-users/<id>",methods = ['GET','POST'])
def edit_property_for_users(id):
    if "loggedin" in session:
        # check if that property is uploaded by the user logged in 
        query ={"_id":ObjectId(id)}
        prop = db.properties.find_one(query)
        if prop['added-by'] == session['id']:
            if request.method  == 'POST':                
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
                pictures = request.files.getlist("images[]") 
                if pictures[0]:
                    filenames = []
                    for picture in pictures:
                        if picture and allowed_file(picture.filename):
                            filename = secure_filename(picture.filename)
                            picture.save(
                                os.path.join(PROPERTIES_FOLDER, filename))
                            filename=filenames.append(filename)                 
                            # compress image and set dimensions
                            # newimage = Image.open(os.path.join(PROPERTIES_FOLDER, str(filename)))
                            # newimage.resize((368, 287))
                            # newimage.save(os.path.join(PROPERTIES_FOLDER, str(filename)), quality=95) 
                        else:
                            return "picture not found or incorrect format"
                            # return render_template("edit-property-for-users.html",username = session['username'],msg=msg)
                    # fetch the last item from the list that is display_pic 
                    display_pic = filenames[-1] 
                    # delete the last item from the list 
                    del filenames[-1]               

                    newData= {
                        "$set" : {
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
                        "display_pic":display_pic,
                        "added-by":session['id'],
                    } 
                    }
                    filter = {'_id': ObjectId(id)}
                    db.properties.update_one(filter, newData)
                    return redirect ("/single-properties/"+id)
                else:
                    newData= {
                        "$set" : {
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
                        "added-by":session['id'],
                    } 
                    }
                    filter = {'_id': ObjectId(id)}
                    db.properties.update_one(filter, newData)
                    return redirect ("/single-properties/"+id)



                
            else:
                query = {'_id': ObjectId(id)}
                propertyData = db.properties.find_one(query)
                # return str(propertyData)
                return render_template("/edit-property-for-users.html",username=session['username'], property=propertyData)    
        else:
            return redirect(url_for("login2"))
    else:
        return redirect(url_for("login2"))

@app.route("/delete-property-for-users/<id>")
def delete_property_for_users(id):
    if "loggedin" in session:
        # check if that property is uploaded by the user logged in 
        query ={"_id":ObjectId(id)}
        prop = db.properties.find_one(query)
        if prop['added-by'] == session['id']:
                query = {'_id': ObjectId(id)}
                db.properties.delete_one(query)
                return redirect("/my-properties/"+session['username'])    
        else:
            return redirect(url_for("login2"))
    else:
        return redirect(url_for("login2"))

@app.route("/mark-property-as-sold/<id>")
def mark_property_as_sold(id):
    if "loggedin" in session:
        # check if that property is uploaded by the user logged in 
        query ={"_id":ObjectId(id)}
        prop = db.properties.find_one(query)
        if prop['added-by'] == session['id']:
                newData= {
                        "$set" : {
                        "sold":True,
                    } 
                    }
                filter = {'_id': ObjectId(id)}
                db.properties.update_one(filter, newData)
                return redirect("/my-properties/"+session['username'])  
        else:
            return redirect(url_for("login2"))
    else:
        return redirect(url_for("login2"))

# -x-x-x-x-x-x-x-x-x-x-x-   ADMIN DASHBOARD START   -x-x-x-x-x-x-x-x-x-x-x- 

@app.route("/admin-dashboard")
def admin_dashboard():    
    if 'loggedin' in session:
        if session['type'] != "admin":
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
            session.pop('type', None)
            return render_template("admin-login.html")
        else:             
            count1 = db.users.count()                 
            count2 = db.agents.count()                 
            count3 = db.properties.count()                 
            count4 = db.contact.count()
            count5 = db.properties.count({'type':'residential'})               
            count6 = db.properties.count({'type':'commercial'})               
            count7 = db.properties.count({'type':'industrial'})               
            count8 = db.properties.count({'type':'vacation'})               
            count9 = db.properties.count({'type':'special'})               
            count10 = db.properties.count({'status':'sale'})               
            count11 = db.properties.count({'status':'rent'})               
            return render_template("dashboard.html",users=count1,agents=count2,properties=count3,messages=count4,residential=count5,commercial=count6,industrial=count7,vacation=count8,special=count9,sale=count10,rent=count11)        
            
    else:
        return render_template("admin-login.html")

@app.route("/admin-login",methods=['GET','POST'])
def admin_login():    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        query = {"username":username}
        adminData = db.admin.find_one(query)
        if adminData:
            if adminData['password'] == password:                
                session['loggedin'] = True
                session['id'] = str(adminData['_id'])
                session['username'] = adminData['username']
                session['type'] = "admin"        
                return redirect(url_for('admin_dashboard'))
            else:
                "Invalid Password"
        else:
            return "Invalid Username"

    else:
        if 'loggedin' in session:
            if session['type'] == "admin":
                return redirect(url_for('admin_dashboard'))
            else:
                render_template("admin-login.html")
        else:
            return render_template("admin-login.html")


@app.route("/users-accounts")
def users_accounts():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            usersData = db.users.find()
            usersLists = []
            for user in usersData:
                user.update({"_id": str(user["_id"])})
                usersLists.append(user)
            return render_template("users-accounts.html",users=usersLists)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/delete-user/<userid>")
def delete_user(userid):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {"_id":ObjectId(userid)}
            userData = db.users.find_one(query)
            if userData:
                db.users.delete_one(query)
                return redirect(url_for('users_accounts'))
            else:
                return "invalid user or user don't exist"
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route("/agents-accounts")
def agents_accounts():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            agentsData = db.agents.find()
            agentsLists = []
            for agent in agentsData:
                agent.update({"_id": str(agent["_id"])})
                agentsLists.append(agent)
            return render_template("agents-accounts.html",agents=agentsLists)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/delete-user/<userid>")
def delete_agents(userid):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {"_id":ObjectId(userid)}
            userData = db.users.find_one(query)
            if userData:
                db.users.delete_one(query)
                return redirect(url_for('users_accounts'))
            else:
                return "invalid user or user don't exist"
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/properties-for-sale")
def properties_for_sale():    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'status':'sale'}
            propertyData = db.properties.find(query)            
            propertyLists = []
            for property in propertyData:
                property.update({"_id": str(property["_id"])})
                propertyLists.append(property)
            return render_template("/property-for-sale.html",properties=propertyLists)
            
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))
@app.route("/properties-for-rent")
def properties_for_rent():    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'status':'rent'}
            propertyData = db.properties.find(query)            
            propertyLists = []
            for property in propertyData:
                property.update({"_id": str(property["_id"])})
                propertyLists.append(property)
            return render_template("/property-for-rent.html",properties=propertyLists)
            
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/edit/property/<id>",methods = ['GET','POST'])
def edit_property(id):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            if request.method == 'POST':
                re
            else:
                query = {'_id': ObjectId(id)}
                propertyData = db.properties.find_one(query)
                return render_template("/edit-property.html",properties=propertyData)            
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/delete-sale-property/<id>")
def delete_sale_property(id):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'_id': ObjectId(id)}
            db.properties.delete_one(query)
            return redirect(url_for('properties_for_sale'))
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/delete-rent-property/<id>")
def delete_rent_property(id):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'_id': ObjectId(id)}
            db.properties.delete_one(query)
            return redirect(url_for('properties_for_rent'))
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/settings')
def settings():    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            admin = db.admin.find_one()
            return render_template("settings.html", admin=admin)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))
 
@app.route('/edit/admin/<id>', methods=['GET', 'POST'])
def edit_admin(id):
        
    if 'loggedin' in session:
        if session['type'] == 'admin':
            if request.method == 'GET':
                # fetch data from admin table 
                query = {'_id': ObjectId(id)}
                admin = db.admin.find_one(query)
                return render_template("edit-admin.html",admin=admin)
            else:
                username = request.form.get("username")
                password = request.form.get("password")
                cpassword = request.form.get("cpassword")
                if cpassword != password:
                    return jsonify({"success":False, "error":"Password didn't match"})
                newvalues = {
                    "$set": {
                        'username': username,
                        'password': password,
                    }
                }
                filter = {'_id': ObjectId(id)}
                db.admin.update_one(filter, newvalues)
                return redirect(url_for('settings')) 
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/messages')
def messages():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            messages = db.contact.find()
            messageLists = []
            for i in messages:
                i.update({"_id": str(i["_id"])})
                messageLists.append(i)
            return render_template('messages.html',messages = messageLists)
    
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/delete-message/<id>")
def delete_message(id):
    if 'loggedin' in session:
        if session['type'] == 'admin': 
            query = {'_id':ObjectId(id)}
            db.contact.delete_one(query)
            return redirect(url_for('messages'))    
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route("/featured-properties")
def featured_properties():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'featured':True}
            featuredProperties = db.properties.find(query)
            Lists = []
            for i in featuredProperties:
                i.update({"_id": str(i["_id"])})
                Lists.append(i)
            return render_template("featured-properties-admin.html",properties=Lists)
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/remove-featured-property/<id>")
def remove_featured_property(id):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'_id':ObjectId(id)}
            Properties = db.properties.find_one(query)
            if Properties:
                newvalues = {"$set": {'featured': False}}
                db.properties.update_one(query, newvalues)
                return redirect(url_for("featured_properties"))                
            else:
                return "Invalid property or Property doesn't exist"
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/feature-a-new-property", methods = ['GET','POST'])
def feature_a_new_property():    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'featured':False}
            nonfeaturedProperties = db.properties.find(query)
            Lists = []
            for i in nonfeaturedProperties:
                i.update({"_id": str(i["_id"])})
                Lists.append(i)
            return render_template("feature-a-new-property.html",properties=Lists)
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/add-to-featured-property/<id>")
def add_to_featured_property(id):    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {'_id':ObjectId(id)}
            Properties = db.properties.find_one(query)
            if Properties:
                newvalues = {"$set": {'featured': True}}
                db.properties.update_one(query, newvalues)
                return redirect(url_for("feature_a_new_property"))                
            else:
                return "Invalid property or Property doesn't exist"
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/reviews")
def reviews():    
    if 'loggedin' in session:
        if session['type'] == 'admin':
            reviews = db.reviews.find()
            Lists = []
            for i in reviews:
                i.update({"_id": str(i["_id"]),"property_id": str(i["property_id"])})
                Lists.append(i)
            return render_template("reviews.html",reviews=Lists)
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/delete-review/<id>")
def delete_review(id):    
    if 'loggedin' in session:
        if session['type'] == 'admin': 
            query = {'_id':ObjectId(id)}
            db.reviews.delete_one(query)
            return redirect(url_for('reviews'))
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))






    

    

if __name__ == '__main__':
    app.run(debug=True)