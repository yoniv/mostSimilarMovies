from flask import Flask, request, render_template, redirect
import app_functions as func
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

mdb = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = mdb['mysql_host']
app.config['MYSQL_USER'] = mdb['mysql_user']
app.config['MYSQL_PASSWORD'] = mdb['mysql_password']
app.config['MYSQL_DB'] = mdb['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movieDetails = request.form
        movie_title = movieDetails['movie']
        return redirect(f'/similar_movies/{movie_title}')
    return render_template('index.html')


@app.route("/similar_movies/<title>")
def hello_world(title):
    same_genre = func.get_same_genre(mysql, title)
    count_of_similar_words = func.get_similar_words(mysql, title)
    the_three_most_similar = func.get_three_most_similar(same_genre, count_of_similar_words)
    return render_template('return_page.html', most_similar=the_three_most_similar)


if __name__=='__main__':
    app.run(debug=True)

