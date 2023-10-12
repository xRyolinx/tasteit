from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import time
import psycopg2
from psycopg2.extras import RealDictCursor

from "../app.py" import app, db, conn

from base64 import b64encode



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
