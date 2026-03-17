from flask import Flask, render_template
from database import fetch_properties,init_db

app = Flask(__name__)

with app.app_context():
    init_db()

#homepage
@app.route("/")
def home():
    name = "Nithyashree"
    properties = fetch_properties()
    return render_template('home.html',username=name,properties = properties)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,debug=True)