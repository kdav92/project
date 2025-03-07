from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    return render_template("survey.html")


@app.route("/results")
def results():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)