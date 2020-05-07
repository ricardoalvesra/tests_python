import os
import requests

from flask import Flask, session, request, render_template, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signin")
def get_signin():
    return render_template("signin.html")


@app.route("/signin", methods=["POST"])
def post_signin():
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount != 0:
        session["username"] = username
        return render_template("index.html")

    return render_template("error.html", message="User not found!")


@app.route("/register")
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message="You can not use this username!")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
               {"username": username, "password": password})
    db.commit()
    
    session["username"] = username

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("index.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'POST':
        text = request.form.get("text")
        books = db.execute("SELECT isbn, title, author, year FROM books WHERE lower(isbn) LIKE :text OR lower(title) LIKE :text OR lower(author) LIKE :text order by title limit 100",
                           {"text": '%'+text.lower()+'%'}).fetchall()

        message = ""
        if len(books) == 0:
            message = "Book not found."

        return render_template("search.html", books=books, message=message)
    else:
        return render_template("search.html")
    
@app.route("/book/<isbn>", methods=["POST", "GET"])
def book(isbn):
    if request.method == 'POST':

        if request.form.get("star") is None:
            return render_template("error.html", message="You must provide a!")

        username = session["username"]
        if db.execute("SELECT * FROM reviews WHERE username = :username and isbn = :isbn", {"username": username, "isbn": isbn}).rowcount != 0:
            return render_template("error.html", message="You can make only one review per book.")

        rating = request.form.get("star")
        description = request.form.get("description")

        db.execute("INSERT INTO reviews (username, isbn, description, rating) VALUES (:username, :isbn, :description, :rating)", {"username": username, "isbn": isbn, "description": description, "rating": rating}
                   )
        db.commit()

    book = db.execute("SELECT isbn, title, author, year FROM books WHERE lower(isbn) LIKE :text", {
        "text": '%'+isbn.lower()+'%'}).fetchone()

    reviews = db.execute("SELECT description, rating, username, isbn FROM reviews WHERE lower(isbn) LIKE :text", {
                         "text": '%'+isbn.lower()+'%'}).fetchall()

    return render_template("book.html", book=book, reviews=reviews, goodreads=get_goodread_rating())


@app.route("/api/<isbn>")
def bookapi(isbn):
    book = db.execute("select count(1), avg(rating), title, author, year, books.isbn from books, reviews where books.isbn = reviews.isbn and lower(books.isbn) LIKE :text group by title, author, year, books.isbn  ", {
        "text": '%' + isbn.lower() + '%'}).fetchone()

    if book is None:
        return jsonify({"status": 404, "message": "book not found"})
    else:
        return jsonify({"title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "isbn": book.isbn,
                    "review_count": book.count,
                    "average_score": str(book.avg)
                    })

def get_goodread_rating():
    response = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "MuE9uBE81jrQ2sdmLfEMMg", "isbns": isbn})
    return response.json()["books"][0]
