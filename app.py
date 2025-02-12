from db import DB
from flask import Flask, render_template, url_for

app = Flask(__name__)




@app.route("/")
def crea_db():
    db=DB()


app.run(debug=True)
