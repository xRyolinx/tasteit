from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import time
import psycopg2
from psycopg2.extras import RealDictCursor
# from flask_socketio import SocketIO, send, emit
from cs50 import SQL
# from werkzeug.utils import secure_filename
from base64 import b64encode

# functions
from helpers.helpers import login_required


# DB
# db = SQL("sqlite:///tasteit.db")

conn, db = None, None
def set_cursor():
    global conn
    global db
    conn = psycopg2.connect(database='tasteit_we38',
                            user='tasteit_we38_user',
                            host='dpg-cor0isnsc6pc73dhc9tg-a.oregon-postgres.render.com',
                            password='l4uwKK5gXF4wlGTchSnQhI49QPysGiyq',
                            keepalives=1,
                            )

    db = conn.cursor(cursor_factory=RealDictCursor)

set_cursor()


# Run flask
app = Flask(__name__)
app.debug = True
app.use_reloader=True

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ------------------------------ DB FUNCTIONS-----------------------
# def select()

# -------------------------- FONCTIONS ---------------------     
            
# Update session
def update_session(id):
    # Values
    db.execute("SELECT * FROM people WHERE id = %s", [id])
    results = db.fetchall()
    person = results[0]
    
    # photo
    decode_photo(person)

    # Save in session
    session['compte'] = person.copy()


# Update person
def decode_photo(person):
    if person['photo']:
        person['photo'] = b64encode(person['photo']).decode("utf-8")


# Update people
def decode_photo_group(people):
    for person in people:
        decode_photo(person)


# ---------------------------------- HOME -------------------------------------

# HOME
@app.route("/")
def home():
    return render_template("home.html", session=session)

@app.route("/home")
def home_redirect():
    return redirect("/")


# -------------------------------- LOGIN -----------------------------------------

# Connexion
@app.route("/signin", methods=["GET", "POST"])
def login():
    # login page
    if request.method == 'GET':
        return render_template("signin.html", session=session)
    
    # Se connecter
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check dans la base de donnees
        check_db = True
        while check_db:
            try:
                db.execute("SELECT * FROM people")
                inscrits = db.fetchall()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        
        for person in inscrits:
            if (username == person["username"]) and (password == person["password"]):
                # Save in session
                update_session(person['id'])
                
                return render_template("loggedin.html", name=username)

        # Non enregistre
        return redirect("/signin")
    
# ------------------------------- DECONNEXION -------------------------------------

# Deconnexion
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if 'compte' in session:
        del session['compte']
    return redirect("/signin")
    

# -------------------------------- INSCRIPTION ---------------------------------------

# Page d'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    # S'inscrire
    if request.method == 'GET':
        return render_template("register.html", session=session)
    
    # Inscrire l'eleve
    if request.method == 'POST':
        # Check if username used
        username = request.form.get("username").replace(' ', '')
        
        check_db = True
        while check_db:
            try:
                db.execute("SELECT id FROM people WHERE username=%s", [username])
                response = db.fetchall()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        
        
        # IF EXISTS
        if response != []:
            return render_template('not_registered.html') 
        
        
        email = request.form.get("email").replace(' ', '')
        password = request.form.get("password").replace(' ', '')

        # photo
        # photo = None
        # img_bytes = request.files["photo"]
        # if img_bytes != None:
            # photo = img_bytes.stream.read()

        # Champs manquants
        if (not username) or (not email) or (not password):
            return render_template("not_registered.html")

        # Inserer
        check_db = True
        while check_db:
            try:
                db.execute("INSERT INTO people (username, email, password, admin) VALUES(%s, %s, %s, 0)",
                            (username, email, password))
                conn.commit()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        

        return render_template("registered.html")

    

# ------------------------------- ADMIN ----------------------------------------

# Afficher les inscrits
@app.route("/inscrits")
@login_required
def registerants():
    # check if admin
    global session
    if session['compte']['admin'] == 0: #NOT ADMIN
        return redirect("/signin")
    
    
    # Inscrits
    db.execute("SELECT * FROM people")
    inscrits = db.fetchall()
    
    # decode photos
    decode_photo_group(inscrits)
        
    return render_template("inscrits.html", registrants=inscrits)


# ------------------------------- FONCTIONNALITÉS -------------------------------------

# --------------------------------- Dishes ------------------------------------------
# Page de plats
@app.route("/dishes", methods=["GET"])
def dishes():
    return render_template("dishes.html", search='', session=session)

# Page de Recherche de plats
@app.route("/dishes/search", methods=["GET"])
def dishes_search():
    # Recherche
    search = request.args.get("q")
    if search == None:
        search = ''
    
    # Html
    return render_template("dishes.html", search=search, session=session)
    

# API DES PLATS
@app.route("/dishes_list", methods=["GET"])
def dishes_list():
    
    # SEARCH
    print('start...')
    search = request.args.get("q")
    
    search = ''
    if (search != None):
        search = (f"name ~* '{search}'")        
        
        
    # Last id
    t = request.args.get("t")
    if (t != None):
        print('fetching last id...')
        
        # La condition de recherche
        if (search == ''):
            condition = ''
        else:
            condition = ' WHERE ' + search
                    
        # Query depuis bdd
        query = 'SELECT MAX(id) as max FROM dishes' + condition
        check_db = True
        while check_db:
            try:
                db.execute(query)
                response = db.fetchall()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        
        response = response[0]['max']
        print('got last id!')
        
        
        # Last id
        last = response
        if response == None:
            last = 0
        
                    
        return str(last)
    
        
        
    # Nombre de plats cherchés
    id = int(request.args.get("id"))
    if (id < 0):
        id = 0
    
    # Condition
    if (search != ''):
        search = search + ' AND'
    condition = search + ' id > ' + str(id)
    
    # Number of results wanted
    nb = int(request.args.get("n"))
    
    # query for sqlite
    
    query = 'SELECT * FROM dishes WHERE ' + condition + ' LIMIT ' + str(nb)
    
    # Selectionner les plats de la bdd
    check_db = True
    while check_db:
        try:
            print('fetching dishes1...')
            db.execute(query)
            
            print('fetching dishes2...')
            plats = db.fetchall()
            
            check_db = False
        except psycopg2.InterfaceError:
            set_cursor()
    print('got dishes!')
        
    
        
    # Trouver le restaurants associé
    for i in range(0,len(plats)):
        check_db = True
        while check_db:
            try:
                db.execute('''SELECT name FROM restaurants WHERE id = 
                   (SELECT restaurant_id from dishes WHERE id = %s)''', [plats[i]["id"]])
                response = db.fetchall()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        
        restau = response[0]["name"]
        
        # Valeur du restau 
        plats[i]["restaurant"] = restau
        
        # Arranger les images
        decode_photo(plats[i])
    
    # end
    return plats
    

# Page d'insertion de plat
@app.route("/dishes/new", methods=["GET", "POST"], endpoint='new_dish')
@login_required
def new_dish():
    db.execute("SELECT name, id FROM restaurants WHERE person_id = %s", [session['compte']['id']])
    restauts = db.fetchall()

    return render_template("new_dish.html", restaurants=restauts)

# Sauvegarder le plat
@app.route("/dishes/insert", methods=["POST"], endpoint='insert_dish')
@login_required
def insert_dish():
    restaurant_id = int(request.form.get("restaurant"))
    nom = request.form.get("name")
    type = request.form.get("type")
    price = int(request.form.get("price"))
    
    img_bytes = request.files["photo"]
    photo = None
    if img_bytes:
        photo = img_bytes.stream.read()
    
    db.execute('''INSERT INTO dishes (restaurant_id, name, type, price, rating, photo)
               VALUES(%s, %s, %s, %s, 0, %s)'''
               , (restaurant_id, nom, type, price, photo))
    
    conn.commit()
    
    return redirect("/dishes")



# --------------------------------- Plat ------------------------------------------

# Page du plat
@app.route("/dish", methods=["GET"])
def dish():
    # Get id
    id = request.args.get("id")
    
    # Get dish from bdd
    db.execute("SELECT * FROM dishes WHERE id = %s", [id])
    plat = db.fetchall()
    
    # Check
    if not plat:
        return "DISH DOESN'T EXIST !"
    
    plat = plat[0]
    
    # If no ingredient
    ingredients = []
    ingredients.append("Inconnu")
    
    plat["ingredients"] = ingredients
    
    
        
    # Get restaurant
    db.execute( '''SELECT name FROM restaurants WHERE id =
                (SELECT restaurant_id FROM dishes WHERE id = %s)
                ''', id)  
    response = db.fetchall()
    restaurant = response[0]["name"]

    # Insert restaurant into plat
    plat["restaurant"] = restaurant
    
    
    # Arranger l'image
    decode_photo(plat)

    # End
    return render_template("dish.html", dish=plat, session=session)
    

    
# --------------------------------- Restaurants ------------------------------------------

# Restaurants
@app.route("/restaurants", methods=["GET"])
def restaurants():
    return render_template("restaurants.html", search='', session=session)


# Page de recherche de restaurants
@app.route("/restaurants/search", methods=["GET"])
def restaurants_search():
    # Recherche
    search = request.args.get("q")
    if search == None:
        search = ''
    
    # Html
    return render_template("restaurants.html", search=search, session=session)
    

# API DES RESTAURANTS
@app.route("/restaurants_list", methods=["GET"])
def restaurants_list():
    
    # SEARCH
    search = request.args.get("q")
    
    if (search != None):
        search = (f"name ~* '{search}'")
    else:
        search = ''
        
        
        
    # Last id
    t = request.args.get("t")
    if (t != None):
        # La condition de recherche
        if (search == ''):
            condition = ''
        else:
            condition = ' WHERE ' + search
                    
        # Query depuis bdd
        query = 'SELECT MAX(id) as max FROM restaurants' + condition
        
        check_db = True
        while check_db:
            try:
                db.execute(query)
                response = db.fetchall()
                check_db = False
            except psycopg2.InterfaceError:
                set_cursor()
        
        response = response[0]['max']
        
        # Last id
        last = response
        if response == None:
            last = 0
        
        # Return 
        return str(last)
    
        
        
    # Nombre de restaurants cherchés
    id = int(request.args.get("id"))
    if (id < 0):
        id = 0
    
    # Condition
    if (search != ''):
        search = search + ' AND'
    condition = search + ' id > ' + str(id)
    
    # Number of results wanted
    nb = int(request.args.get("n"))
    
    # query from sqlite
    query = 'SELECT * FROM restaurants WHERE ' + condition + ' LIMIT ' + str(nb)
    
    # Selectionner les restaurants de la bdd
    check_db = True
    while check_db:
        try:
            db.execute(query)
            plats = db.fetchall()
            check_db = False
        except psycopg2.InterfaceError:
            set_cursor()
    
        
    # Arranger les images
    for plat in plats:
        if plat['photo'] != None:
            plat['photo'] = b64encode(plat['photo']).decode("utf-8")
    
    return plats
    

# Page d'insertion de restaurant
@app.route("/restaurants/new", methods=["GET", "POST"], endpoint='new_restaurant')
@login_required
def new_restaurant():
    return render_template("new_restaurant.html")

# Sauvegarder le restaurant
@app.route("/restaurants/insert", methods=["POST"], endpoint='insert_restaurant')
@login_required
def insert_restaurant():
    id = session['compte']['id']
    nom = request.form.get("name")
    type = request.form.get("type")
    adress = request.form.get("adress")
    
    img_bytes = request.files["photo"]
    photo = None
    if img_bytes:
        photo = img_bytes.stream.read()
    
    db.execute('''
                    INSERT INTO restaurants (person_id, name, type, work_hours, work_days, adress, rating, photo)
                    VALUES(%s, %s, %s, 0, 0, %s, 0, %s)
               ''', (id, nom, type, adress, photo))
    conn.commit()
    
    return redirect("/restaurants")



# --------------------------------- Un Restaurant ------------------------------------------

# Page du Restaurant
@app.route("/restaurant", methods=["GET"])
def restaurant():
    # Get id
    id = request.args.get("id")
    
    # Get restaurant from bdd
    db.execute("SELECT * FROM restaurants WHERE id = %s", [id])
    restau = db.fetchall()
    
    # Check
    if (restau == []):
        return "RESTAURANT DOESN'T EXIST !"
    
    # Simplify from array (bcz only one element)
    restau = restau[0]


    
    # Get specialities
    # db.execute('''SELECT name FROM specialities WHERE id IN
    #             (SELECT speciality_id FROM restaurant_speciality WHERE restaurant_id = %s);
    #             ''', [id])
    # specialities_list = db.fetchall()
    
    # If no restaurant
    specialities = []
    specialities.append("Inconnu")
    # else
    # if (specialities_list != []): 
    #     # From dict to array
    #     specialities = []
    #     for speciality in specialities_list:
    #         specialities.append(speciality["name"])

    # Insert ingredients into plat
    restau["specialities"] = specialities
    
    
    
    # Arranger l'image
    if restau['photo'] != None:
        restau['photo'] = b64encode(restau['photo']).decode("utf-8")
    

    # End
    return render_template("restaurant.html", restaurant=restau, session=session)



# ------------------------------ Contact us ----------------------------------------
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contactus.html", session=session)



# ------------------------------- Profil ----------------------------------
@app.route("/info", methods=["GET", "POST"], endpoint='info')
@login_required
def info():
    person = session['compte']
    for key in person:
        if not person[key]:
            person[key] = ''
            
    return render_template("profil.html", person=person, adr='info')
    
@app.route("/profil", methods=["GET", "POST"], endpoint='profil')
@login_required
def profil():
    # Normal page
    if request.method == 'GET':            
        person = session['compte']
        for key in person:
            if not person[key]:
                person[key] = ''
        return render_template("profil.html", person=person, adr='profil')

    # Update page
    if request.method == 'POST':
        # UPDATE photo
        photo = request.files.get('photo')
        print(photo)
        if photo:
            print('h')
            id = session['compte']['id']
            photo = photo.stream.read()
            
            # Add to database
            db.execute("UPDATE people SET photo = %s WHERE id = %s", (photo, id))
            conn.commit()
            
            # Save in session
            update_session(id)
            
            return {
                'rep' : 'ok',
            }
            
        
        # UPDATE INFO
        id = session['compte']['id']
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        adress = request.form.get("adress")
        phone = request.form.get("phone")
        email = request.form.get("email")
        
        # Check if username not used
        # Response to JS (DEFAULT IS OK)
        check_username = {
            'check' : True,
            'value' : username
        }
        # Search in DB
        db.execute("SELECT id FROM people WHERE username=%s", [username])
        response = db.fetchall()
        
        # DOESN'T EXIST
        if response == []:
            # Update
            db.execute("UPDATE people SET username=%s WHERE id=%s", (username, id))
            conn.commit()
        else:
            # Response to JS (NOT OK)
            db.execute("SELECT username FROM people WHERE id=%s", [id])
            username = db.fetchall()
            
            check_username = {
                'check' : False,
                'value' : username[0]['username']
            }
            

        # Update DB
        db.execute('''UPDATE people SET
                   password=%s, first_name=%s, last_name=%s, adress=%s, phone=%s, email=%s
                   WHERE id=%s''',(password, first_name, last_name, adress, phone, email ,id))
        
        
        # Save in session
        update_session(id)
        
        return check_username
    
    
# ------------------------------ MESSAGES ----------------------------

@app.route("/messages", methods=["GET", "POST"], endpoint='messages')
@login_required
def messagerie():
    # Get all people
    db.execute('SELECT * FROM people')
    people = db.fetchall()
    decode_photo_group(people)
    # print(people)
    
    return render_template('messages.html', person=session['compte'], people=people, adr='messages', id=0)


# ----------------------------- ENVOYER MSG ------------------------------
@app.route('/send', methods=['POST'], endpoint='send_msg')
@login_required
def send():
    # Id of logged account
    id = session['compte']['id']
    # Data sent
    id_destinataire = request.form.get('id_destinataire')
    msg = request.form.get('msg')
    
    # Send to db
    db.execute("INSERT INTO messages (id_sent, message, id_received) VALUES (%s, %s, %s)",
               (id, msg, id_destinataire))
    conn.commit()

    # end
    return {'status' : 'ok'}

# -------------------------------- Receiving messages ----------------------------------
@app.route('/receive', methods=['POST'], endpoint='receive_msg')
@login_required
def receive():
    
    # Id of logged account
    id = session['compte']['id']
    # Data sent
    id_destinataire = request.form.get('id_destinataire')
    last_id = request.form.get('last_id')
    
            
    # Search
    db.execute('''SELECT * FROM messages WHERE ((id > %s) AND
                (
                    (%s = id_sent AND %s = id_received)
                    OR
                    (%s = id_received AND %s = id_sent)
                ))
                ORDER BY id ASC''', (last_id, id, id_destinataire, id, id_destinataire)) 
    responses = db.fetchall()
    
    # Send response 
    if responses != []:
        return {
            'status' : True,
            'data' : responses
        }
    else:
        return {
            'status' : False
        }
    
    
    
# --------------------------- MES RESTAURANTS -----------------------------
@app.route('/mes-restaurants', methods=['GET', 'POST'], endpoint='mes restaurants')
@login_required
def mes_restaurants_view():
    db.execute('SELECT id, name FROM restaurants WHERE person_id = %s', [session['compte']['id']])
    restauts = db.fetchall()
    
    for restau in restauts:
        db.execute('SELECT name FROM dishes WHERE restaurant_id = %s', [restau['id']])
        plats = db.fetchall()
        restau['plats'] = plats
    
    return render_template('mes_restaurants.html', person=session['compte'], restaurants=restauts)