
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["school"]

# Collection
students = db["students"]


@app.route("/")
def home():
    all_students = list(students.find())
    return render_template("index.html", students=all_students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name")
    age = request.form.get("age")

    if name and age:
        students.insert_one({
            "name": name,
            "age": int(age)
        })

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
