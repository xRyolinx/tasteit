from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import time

# from flask_socketio import SocketIO, send, emit

from cs50 import SQL

# from werkzeug.utils import secure_filename
from base64 import b64encode


# DB
db = SQL("sqlite:///tasteit.db")

# Run flask
app = Flask(__name__)
app.debug = True
app.use_reloader=True

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# -------------------------- FONCTIONS ---------------------

# Convert none values to ''
def convertion(dictionnaire):
    for key in dictionnaire:
        if (dictionnaire[key] == None) or (dictionnaire[key] == 'None'):
            dictionnaire[key] = ''
            

# Update session
def update_session(id):
    # Values
    results = db.execute("SELECT * FROM people WHERE id = ?", id)
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
    inscrits = db.execute("SELECT * FROM people")
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
        # Sauvergarder l'eleve
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # PDP
        pdp = None
        # img_bytes = request.files["pdp"]
        # if img_bytes != None:
            # pdp = img_bytes.stream.read()

        # Champs manquants
        if (not username) or (not email) or (not password):
            return render_template("not_registered.html")

        # Inserer
        db.execute("INSERT INTO people (username, email, password, pdp, admin) VALUES(?, ?, ?, ?, 0)",
                username, email, password, pdp)

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
    inscrits = db.execute("SELECT * FROM people")
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
        session.pop('compte')
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
        search = "name LIKE '%" + search + "%'"
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
        response = db.execute(query)
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
    plats = db.execute(query)
    
    # Trouver les restaurants associés
    for i in range(0,len(plats)):
        restauts = db.execute( '''SELECT name FROM restaurants WHERE id =
                                (SELECT restaurant_id FROM restaurant_dish WHERE dish_id = ?)
                                ''', plats[i]["id"])
        
        # Valeur du restau
        restaurant = "Inconnu"
        if (restauts != []):        
            restaurant = restauts[0]["name"]
            
        plats[i]["restaurant"] = restaurant
        
    # Arranger les images
    for plat in plats:
        if plat['photo'] != 0:
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
    
    db.execute('''
                    INSERT INTO dishes (name, type, price, rating, photo)
                    VALUES(?, ?, ?, 0, ?)
               ''', nom, type, price, photo)
    
    return redirect("/dishes")



# --------------------------------- Plat ------------------------------------------

# Page du plat
@app.route("/dish", methods=["GET"])
def dish():
    # Get id
    id = request.args.get("id")
    
    # Get dish from bdd
    plat = db.execute("SELECT * FROM dishes WHERE id = ?", id)
    
    # Check
    if (plat == []):
        return "DISH DOESN'T EXIST !"
    
    # Simplify from array (bcz only one element)
    plat = plat[0]


    
    # Get ingredients
    ingredients_list = db.execute('''SELECT name FROM ingredients WHERE id IN
                             (SELECT ingredient_id FROM dish_ingredient WHERE dish_id = ?);
                             ''', id)
    
    # If no ingredient
    ingredients = []
    ingredients.append("Inconnu")
    # else
    if (ingredients_list != []): 
        # From dict to array
        ingredients = []
        for ingredient in ingredients_list:
            ingredients.append(ingredient["name"])

    # Insert ingredients into plat
    plat["ingredients"] = ingredients
    
    
        
    # Get restaurant
    restauts = db.execute( '''SELECT name FROM restaurants WHERE id =
                                (SELECT restaurant_id FROM restaurant_dish WHERE dish_id = ?)
                                ''', id)  
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
        search = "name LIKE '%" + search + "%'"
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
        response = db.execute(query)
        
        # Last id
        if response == []:
            last = 0
        else:
            last = response[0]["max"]
            
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
    plats = db.execute(query)
        
    # Arranger les images
    for plat in plats:
        if plat['photo'] != 0:
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
                    VALUES(?, ?, 0, 0, ?, 0, ?)
               ''', nom, type, adress, photo)
    
    return redirect("/restaurants")



# --------------------------------- Un Restaurant ------------------------------------------

# Page du Restaurant
@app.route("/restaurant", methods=["GET"])
def restaurant():
    # Get id
    id = request.args.get("id")
    
    # Get restaurant from bdd
    restau = db.execute("SELECT * FROM restaurants WHERE id = ?", id)
    
    # Check
    if (restau == []):
        return "RESTAURANT DOESN'T EXIST !"
    
    # Simplify from array (bcz only one element)
    restau = restau[0]


    
    # Get specialities
    specialities_list = db.execute('''SELECT name FROM specialities WHERE id IN
                             (SELECT speciality_id FROM restaurant_speciality WHERE restaurant_id = ?);
                             ''', id)
    
    # If no restaurant
    specialities = []
    specialities.append("Inconnu")
    # else
    if (specialities_list != []): 
        # From dict to array
        specialities = []
        for speciality in specialities_list:
            specialities.append(speciality["name"])

    # Insert ingredients into plat
    restau["specialities"] = specialities
    
    
    
    # Arranger l'image
    if restau['photo'] != 0:
        restau['photo'] = b64encode(restau['photo']).decode("utf-8")
    

    # End
    return render_template("restaurant.html", restaurant=restau, session=session)



# ------------------------------ About us ----------------------------------------
@app.route("/aboutus", methods=["GET"])
def aboutus():
    return render_template("aboutus.html", session=session)



# ------------------------------- Profil ----------------------------------
@app.route("/profil", methods=["GET", "POST"])
def profil():
    # Normal page
    if request.method == 'GET':
        if 'compte' not in session:
            return redirect("/signin") 
        
        return render_template("profil.html", person=session['compte'])
    
    # Update page
    if request.method == 'POST':
        # UPDATE PDP
        pdp = request.files.get('pdp')
        if pdp != None:
            id = request.form.get('id')
            pdp = pdp.stream.read()
            
            # Add to database
            db.execute("UPDATE people SET pdp = ? WHERE id = ?", pdp, id)
            
            # Save in session
            update_session(id)
            
            return {
                'rep' : 'ok',
            }
            
        
        # UPDATE INFO
        id = request.form.get("id")
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
        response = db.execute("SELECT id FROM people WHERE username=?", username)
        # DOESN'T EXIST
        if response == []:
            # Update
            db.execute("UPDATE people SET username=? WHERE id=?", username, id)
        else:
            # Response to JS (NOT OK)
            username = db.execute("SELECT username FROM people WHERE id=?", id)
            check_username = {
                'check' : False,
                'value' : username[0]['username']
            }
            

        # Update DB
        db.execute('''UPDATE people SET
                   password=?, first_name=?, last_name=?, adress=?, phone=?, email=?
                   WHERE id=?''',password, first_name, last_name, adress, phone, email ,id)
        
        
        # Save in session
        update_session(id)
        
        return check_username
    

# ------------------------------ MESSAGES ----------------------------
@app.route("/messages", methods=["GET", "POST"])
def messagerie():
    # Get all people
    people = db.execute('SELECT * FROM people')
    update_people(people)
    
    return render_template('messages.html', person=session['compte'], people=people)


# ---------------------------------- ENVOYER MSG ------------------------------
@app.route('/send', methods=['POST'])
def send():
    # Id of logged account
    id = session['compte']['id']
    # Data sent
    id_destinataire = request.form.get('id_destinataire')
    msg = request.form.get('msg')
    
    # Send to db
    db.execute("INSERT INTO messages (id_sent, message, id_received) VALUES (?, ?, ?)", id, msg, id_destinataire)

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
    responses = db.execute('''
                            SELECT * FROM messages WHERE ((id > ?) AND
                            (
                                (? = id_sent AND ? = id_received)
                                OR
                                (? = id_received AND ? = id_sent)
                            ))
                        ORDER BY id ASC''', last_id, id, id_destinataire, id, id_destinataire) 
    
    # Send response 
    if responses != []:
        print(responses)
        return {
            'status' : True,
            'data' : responses
        }
    else:
        return {
            'status' : False,
        }
    
@app.route('/poll', methods=['POST'])
def poll():    
    # Prepare return value if false
    ret = {
        'status' : False
    }
    
    # Data sent
    id = session['compte']['id']
    id_destinataire = request.form.get('id_destinataire')
    stop = request.form.get('stop')
    
    # First run
    if id_destinataire == '0':
        # print('START')
        return ret
        
    
    # Stop
    if stop == 'true':
        db.execute('UPDATE receive SET val = ? WHERE id_user = ? AND id_dest = ?', 'false', id, id_destinataire)
        # print('receive = false !')
        return ret
    
    # Last id sent
    last_id = request.form.get('last_id')
    
    # Initialize Request
    results = db.execute('SELECT * FROM receive WHERE id_user = ? AND id_dest = ?', id, id_destinataire)
    if results == []:
        db.execute('INSERT INTO receive (id_user, id_dest, val) VALUES (?, ?, ?)', id, id_destinataire,'true')
    else:
        db.execute('UPDATE receive SET val = ? WHERE id_user = ? AND id_dest = ?', 'true', id, id_destinataire)
    
    # Search
    while True:
        val = db.execute('SELECT val FROM receive WHERE id_user = ? AND id_dest = ?', id, id_destinataire)
        val = val[0]['val']
        # print(val)
        if val == 'false':
            break
        
        # Search
        responses = db.execute('''
                                SELECT * FROM messages WHERE ((id > ?) AND
                                (
                                    (? = id_sent AND ? = id_received)
                                    OR
                                    (? = id_received AND ? = id_sent)
                                )
                            )''', last_id, id, id_destinataire, id, id_destinataire) 
        
        # print(id_destinataire)
        # Result
        if responses != []:
            # emit('receive', responses)
            return {
                'status' : True,
                'data' : responses
            }
            
        # Wait a little
        time.sleep(0.1)
    
    # End
    # print('REQUEST ARRESTED')
    return ret

