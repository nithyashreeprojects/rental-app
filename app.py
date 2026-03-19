from flask import Flask, render_template,request
from database import fetch_properties,init_db,get_connection
from matcher import get_matches

app = Flask(__name__)

with app.app_context():
    init_db()

#homepage
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/listings")
def listings():
    properties=fetch_properties()
    return render_template('listings.html',properties=properties)

@app.route("/property/<int:id>")
def property_detail(id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE id = ?", (id,))
    property = cursor.fetchone()
    conn.close()
    if property is None:
        return "Property not found" , 404
    return render_template('property.html',property=property)

@app.route("/match")
def match():
    return render_template('match.html')

@app.route("/results",methods=["POST"])
def results():
    preferences={
        "city":request.form.get("city","Chennai"),
        "area":request.form.get("area",""),
        "max_budget":int(request.form.get("max_budget",50000)),
        "bedrooms":int(request.form.get("bedrooms",1)),
        "furnishing_type":request.form.get("furnishing_type",""),
        "has_parking":int(request.form.get("has_parking",0)),
        "has_lift":int(request.form.get("has_lift",0)),
        "pets_allowed":int(request.form.get("pets_allowed",0)),
        "maintenance_included":int(request.form.get("maintenance_included",0)),
    }
    properties = fetch_properties()
    matches=get_matches(properties,preferences)
    return render_template('results.html',matches=matches,preferences=preferences)

if __name__=='__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)