
import re

from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
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
    q = request.args.get("q", "").strip()
    age_range = request.args.get("age_range", "").strip()

    query = {}

    if q:
        query["name"] = {"$regex": re.escape(q), "$options": "i"}

    if age_range:
        try:
            low, high = age_range.split("-")
            query["age"] = {"$gte": int(low), "$lt": int(high)}
        except (ValueError, TypeError):
            pass

    all_students = list(students.find(query))
    return render_template("index.html", students=all_students, q=q, age_range=age_range)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name")
    age = request.form.get("age")

    if name and age:
        students.insert_one({
            "name": name,
            "age": int(age)
        })

    return redirect(url_for("home"))


@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        students.delete_one({"_id": ObjectId(student_id)})
    except Exception:
        pass

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
