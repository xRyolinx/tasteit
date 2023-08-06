from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import time
import psycopg2
from psycopg2.extras import RealDictCursor

# from flask_socketio import SocketIO, send, emit

from cs50 import SQL

# from werkzeug.utils import secure_filename
from base64 import b64encode


# DB
# db = SQL("sqlite:///tasteit.db")
conn = psycopg2.connect(database='tasteit', user='tasteit_user', host='dpg-cijh0senqql0l1rkun1g-a.frankfurt-postgres.render.com', password='Kp2hBNSkUL6ZKyV0jyPGUeu14sXWSpl4')
db = conn.cursor(cursor_factory=RealDictCursor)


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

# Convert none values to ''
def convertion(dictionnaire):
    for key in dictionnaire:
        if (dictionnaire[key] == None) or (dictionnaire[key] == 'None'):
            dictionnaire[key] = ''
            
            
# Update session
def update_session(id):
    # Values
    db.execute("SELECT * FROM people WHERE id = %s", [id])
    results = db.fetchall()
    person = results[0]
    # PDP
    update_person(person)
    # Blank
    convertion(person)

    # Save in session
    session['compte'] = person.copy()


# Update person
def update_person(person):
    if person['pdp'] != None:
            person['pdp'] = b64encode(person['pdp']).decode("utf-8")


# Update people
def update_people(people):
    for person in people:
        update_person(person)
        convertion(person)


# ---------------------------------- HOME -------------------------------------

# HOME
@app.route("/")
def home():
    return render_template("home.html", session=session)

@app.route("/home")
def home_red():
    return redirect("/")


# -------------------------------- LOGIN -----------------------------------------

# Connexion
@app.route("/signin", methods=["GET", "POST"])
def login():
    return render_template("signin.html", session=session)


# Loggedin
@app.route("/loggedin", methods=["GET", "POST"])
def loggedin():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Check dans la base de donnees
    db.execute("SELECT * FROM people")
    inscrits = db.fetchall()
    
    for person in inscrits:
        if (username == person["username"]) and (password == person["password"]):
            # Save in session
            update_session(person['id'])
            
            return render_template("loggedin.html", name=username)

    # Non enregistre
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
        db.execute("SELECT id FROM people WHERE username=%s", [username])
        response = db.fetchall()
        
        # IF EXISTS
        if response != []:
            return render_template('not_registered.html') 
        
        
        email = request.form.get("email").replace(' ', '')
        password = request.form.get("password").replace(' ', '')

        # PDP
        # pdp = None
        # img_bytes = request.files["pdp"]
        # if img_bytes != None:
            # pdp = img_bytes.stream.read()

        # Champs manquants
        if (not username) or (not email) or (not password):
            return render_template("not_registered.html")

        # Inserer
        db.execute("INSERT INTO people (username, email, password, admin) VALUES(%s, %s, %s, 0)",
                (username, email, password))
        conn.commit()

        return render_template("registered.html")

    

# ------------------------------- ADMIN ----------------------------------------

# Afficher les inscrits
@app.route("/inscrits")
def registerants():
    # If not connected
    global session
    if 'compte' not in session: #NOT LOGGED IN
        return redirect("/signin")
    if session['compte']['admin'] == 0: #NOT ADMIN
        return redirect("/signin")
    
    
    # Inscrits
    db.execute("SELECT * FROM people")
    inscrits = db.fetchall()
    
    for person in inscrits:
        # Convert types of none
        convertion(person)
        
        # pdp
        if person['pdp'] != '':
            person['pdp'] = b64encode(person['pdp']).decode("utf-8")
        

    return render_template("inscrits.html", registrants=inscrits)


# ------------------------------- DECONNEXION -------------------------------------

# Deconnexion
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if 'compte' in session:
        session.clear()
    return redirect("/signin")


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
        query = 'SELECT MAX(id) as max FROM dishes' + condition
        db.execute(query)
        response = db.fetchall()
        response = response[0]['max']
        
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
    db.execute(query)
    plats = db.fetchall()
    
    # Trouver les restaurants associés
    for i in range(0,len(plats)):
        db.execute('''SELECT name FROM restaurants WHERE id =
                   (SELECT restaurant_id FROM restaurant_dish WHERE dish_id = %s)'''
                   , [plats[i]["id"]])
        
        restauts = db.fetchall()
        
        # Valeur du restau
        restaurant = "Inconnu"
        if (restauts != []):        
            restaurant = restauts[0]["name"]
            
        plats[i]["restaurant"] = restaurant
        
    # Arranger les images
    for plat in plats:
        if plat['photo'] != None:
            plat['photo'] = b64encode(plat['photo']).decode("utf-8")
    
    return plats
    

# Page d'insertion de plat
@app.route("/dishes/new", methods=["GET", "POST"])
def new_dish():
    return render_template("new_dish.html")

# Sauvegarder le plat
@app.route("/dishes/insert", methods=["POST"])
def insert_dish():
    nom = request.form.get("name")
    type = request.form.get("type")
    price = int(request.form.get("price"))
    
    img_bytes = request.files["photo"]
    photo = img_bytes.stream.read()
    
    db.execute('''INSERT INTO dishes (name, type, price, rating, photo) VALUES(%s, %s, %s, 0, %s)'''
               , (nom, type, price, photo))
    
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
    if (plat == []):
        return "DISH DOESN'T EXIST !"
    
    # Simplify from array (bcz only one element)
    plat = plat[0]


    
    # Get ingredients
    # db.execute('''SELECT name FROM ingredients WHERE id IN
    #             (SELECT ingredient_id FROM dish_ingredient WHERE dish_id = %s);
    #             ''', id)
    
    # ingredients_list = db.fetchall()
    
    # If no ingredient
    ingredients = []
    ingredients.append("Inconnu")
    # # else
    # if (ingredients_list != []): 
    #     # From dict to array
    #     ingredients = []
    #     for ingredient in ingredients_list:
    #         ingredients.append(ingredient["name"])

    # Insert ingredients into plat
    plat["ingredients"] = ingredients
    
    
        
    # Get restaurant
    db.execute( '''SELECT name FROM restaurants WHERE id =
                (SELECT restaurant_id FROM restaurant_dish WHERE dish_id = %s)
                ''', id)  
    restauts = db.fetchall()
    
    # Check
    restaurant = "Inconnu"
    if (restauts != []):        
        restaurant = restauts[0]["name"]

    # Insert restaurant into plat
    plat["restaurant"] = restaurant
    
    
    # Arranger l'image
    if plat['photo'] != 0:
        plat['photo'] = b64encode(plat['photo']).decode("utf-8")
    

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
        db.execute(query)
        
        response = db.fetchall()
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
    db.execute(query)
    plats = db.fetchall()
        
    # Arranger les images
    for plat in plats:
        if plat['photo'] != None:
            plat['photo'] = b64encode(plat['photo']).decode("utf-8")
    
    return plats
    

# Page d'insertion de restaurant
@app.route("/restaurants/new", methods=["GET", "POST"])
def new_restaurant():
    return render_template("new_restaurant.html")

# Sauvegarder le restaurant
@app.route("/restaurants/insert", methods=["POST"])
def insert_restaurant():
    nom = request.form.get("name")
    type = request.form.get("type")
    adress = request.form.get("adress")
    
    img_bytes = request.files["photo"]
    photo = img_bytes.stream.read()
    
    db.execute('''
                    INSERT INTO restaurants (name, type, work_hours, work_days, adress, rating, photo)
                    VALUES(%s, %s, 0, 0, %s, 0, %s)
               ''', (nom, type, adress, photo))
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
@app.route("/info", methods=["GET", "POST"])
def info():
    return render_template("profil.html", person=session['compte'], adr='info')
    
@app.route("/profil", methods=["GET", "POST"])
def profil():
    # Normal page
    if request.method == 'GET':
        if 'compte' not in session:
            return redirect("/signin") 
        
        return render_template("profil.html", person=session['compte'], adr='profil')
    
    # Update page
    if request.method == 'POST':
        # UPDATE PDP
        pdp = request.files.get('pdp')
        if pdp != None:
            id = session['compte']['id']
            pdp = pdp.stream.read()
            
            # Add to database
            db.execute("UPDATE people SET pdp = %s WHERE id = %s", (pdp, id))
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

@app.route("/messages", methods=["GET", "POST"])
def messagerie():
    # Get all people
    db.execute('SELECT * FROM people')
    people = db.fetchall()
    update_people(people)
    # print(people)
    
    return render_template('messages.html', person=session['compte'], people=people, adr='messages', id=0)


# ----------------------------- ENVOYER MSG ------------------------------
@app.route('/send', methods=['POST'])
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
@app.route('/receive', methods=['POST'])
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
    