from flask import Flask, render_template, url_for, request
from flask_googlemaps import GoogleMaps, Map
import sqlite3
import requests


#from facebook_scrapper import get_posts
app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyA4AkTJLdwf4DKt9DjEH4J2iQXv1E_emjU'
GoogleMaps(app)
#facebook_posts = []
#conn = sqlite3.connect('hawkerhelp.db') 
#c = conn.cursor()

#for post in get_posts(group = '268960887438286', pages = 1):
#    facebook_posts.append(post)

def get_coordinates(API_KEY, address_text):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + address_text
        + "&key="
        + API_KEY
    ).json()
    return response["results"][0]["geometry"]["location"]


# shows page about what HawkerHelp is
@app.route("/") 
def index():
    return render_template("index.html")

# actual main page with search and everything
@app.route('/shop')
def shop():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers")
    return render_template('shoptes.html', results = results)

@app.route('/search')
def search():
    search = request.args.get('search')
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers WHERE StallName LIKE '%" + search + "%' OR StallCuisine LIKE '%"+ search + "%';").fetchall()
    #print(results)
    #print(rows)
    return render_template('search.html',results = results)


@app.route('/sataymankim')
def hawker1():
    location = 'Blk 261 Serangoon Central Drive'
    if (location != ''):
        coords = get_coordinates('AIzaSyA4AkTJLdwf4DKt9DjEH4J2iQXv1E_emjU', location)
    latitude = coords['lat']
    longitude = coords['lng']
    mymap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        markers=[(latitude, longitude)],
        style='height:350px;width:800px;margin:0;'
    )
    return render_template('hawker1.html', mymap=mymap)

@app.route('/songkeefishball')
def hawker2():
    return render_template("hawker2.html")

@app.route("/chinese")
def chinese():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers WHERE StallCuisine LIKE '%chinese%';").fetchall()
    return render_template("search.html", results=results)

@app.route("/malay")
def malay():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers WHERE StallCuisine LIKE '%malay%';").fetchall()
    return render_template("search.html", results=results)

@app.route("/indian")
def indian():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers WHERE StallCuisine LIKE '%indian%';").fetchall()
    return render_template("search.html", results=results)

@app.route("/western")
def western():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute("SELECT * FROM Hawkers WHERE StallCuisine LIKE '%western%';").fetchall()
    return render_template("search.html", results=results)

@app.route("/others")
def others():
    conn = sqlite3.connect('hawkerhelp.db') 
    c = conn.cursor()
    results = c.execute('''
        SELECT * FROM Hawkers WHERE StallCuisine NOT LIKE "%western%" 
        AND StallCuisine NOT LIKE "%chinese%" AND 
        StallCuisine NOT LIKE "%malay%" AND StallCuisine NOT LIKE "%indian%";''').fetchall()
    return render_template("search.html", results=results)



'''
@app.route("/sataymankim", methods=['POST', 'GET'])
def view():
    if request.method == 'POST':
        location = request.form["location"]
        location = location.strip()
        if (location != ''):
            coords = get_coordinates('AIzaSyA4AkTJLdwf4DKt9DjEH4J2iQXv1E_emjU', location)
        latitude = coords['lat']
        longitude = coords['lng']
    mymap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        markers=[(latitude, longitude)]
    )
    return render_template('hawker1.html', mymap=mymapp)
    '''


if __name__ == "__main__":
    app.run(debug = True)