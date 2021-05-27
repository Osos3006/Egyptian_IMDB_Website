from flask import Flask, request, jsonify, render_template, redirect
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11409629'
app.config['MYSQL_PASSWORD'] = '8kdfymBTMK'
app.config['MYSQL_DB'] = 'sql11409629'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JSON_AS_ASCII'] = False

mysql = MySQL(app)

logged_user = None


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/', methods=['POST'])
def check_login():
    UN = request.form['username']
    PW = request.form['password']
    cur = mysql.connection.cursor()
    query = f'''SELECT UserName , Password from user WHERE UserName="{UN}" AND Password="{PW}";'''
    cur.execute(query)
    data = cur.fetchall()
    if (len(data) == 1):
        global logged_user
        logged_user = UN
        return render_template("index.html", username=UN)
    else:
        return redirect('/register')


@app.route('/register', methods=['POST', 'GET'])
def register():
    '''
    if not request.form or not 'username' in request.form \
            or not 'Email' in request.form or not 'password' in request.form \
            or not 'DateOfBirth' in request.form \
            or not 'Gender' in request.form:

        return 'a field is missing', 400
        '''

    if request.method == 'POST':
        Email = request.form['Email']
        UN = request.form['username']
        PW = request.form['password']
        DOB = request.form['DateOfBirth']
        Gender = request.form['Gender']

        if not Email or not UN or not PW or not DOB or not Gender:
            return 'a field is missing', 400

        cur = mysql.connection.cursor()
        check_query = f'SELECT * FROM user WHERE EmailAddress="{Email}" OR UserName = "{UN}"'
        cur.execute(check_query)
        duplicates = cur.fetchall()
        if len(duplicates) != 0:
            return 'duplicate username or email', 409
        query = f'''INSERT INTO user VALUES ("{Email}", "{UN}" , "{Gender}", "{DOB}", "{PW}")'''
        cur.execute(query)
        mysql.connection.commit()
        global logged_user
        logged_user = UN
        return render_template("index.html", username=UN)
    return render_template("register.html")


@app.route('/movies')
def movies():
    cur = mysql.connection.cursor()
    query = "select * from movie;"
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        if row['MovieDescription'] is not "NONE" and row[
                'MovieDescription'] is not None:
            row['MovieDescription'] = row['MovieDescription'].strip()
        if row['ReleaseDate'] is not "NONE":
            row['ReleaseDate'] = row['ReleaseDate']
        if row['TotalRevenue'] is not "NONE":
            row['TotalRevenue'] = str(row['TotalRevenue'])
        if row['AVG_RATING'] is not "NONE":
            row['AVG_RATING'] = str(row['AVG_RATING'])

    return render_template("movies.html", data=data)


@app.route('/movies/<int:movie_id>')
def movie(movie_id):
    cur = mysql.connection.cursor()
    query = f"select * from movie WHERE id={movie_id};"
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        if row['MovieDescription'] is not "NONE" and row[
                'MovieDescription'] is not None:
            row['MovieDescription'] = row['MovieDescription'].strip()
        if row['ReleaseDate'] is not "NONE":
            row['ReleaseDate'] = row['ReleaseDate']
        if row['TotalRevenue'] is not "NONE":
            row['TotalRevenue'] = str(row['TotalRevenue'])
        if row['AVG_RATING'] is not "NONE":
            row['AVG_RATING'] = str(row['AVG_RATING'])
        if row['AgeRating'] is None:
            row['AgeRating'] = "NONE"
        if row['PremiereDate'] is None:
            row['PremiereDate'] = "NONE"

    query = f"select * from moviegenre WHERE movieID={movie_id};"
    cur.execute(query)
    genre = cur.fetchall()
    return render_template("movie.html", data=data, genre=genre)


@app.route('/movies/<int:movie_id>', methods=['POST'])
def add_rev(movie_id):
    rev = request.form['review']
    rate = request.form['rate']
    if not rev:
        return "empty review", 400
    cur = mysql.connection.cursor()
    query = f'''INSERT INTO review VALUES ("{rate}", "{rev}" , "{movie_id}", "{logged_user}")'''
    cur.execute(query)
    mysql.connection.commit()
    return redirect(f'/movies/{movie_id}')


@app.route('/movies/<int:movie_id>/reviews')
def get_reviews(movie_id):
    cur = mysql.connection.cursor()
    query = f"SELECT UserName , RateValue , TextualReview from review r WHERE r.movieID = {movie_id};"
    cur.execute(query)
    data = cur.fetchall()
    query = f"select m.MovieName from movie m where m.ID={movie_id}"
    cur.execute(query)
    name = cur.fetchall()
    return render_template("review.html", data=data, name=name)


@app.route('/movies/<int:movie_id>/cast')
def get_movie_cast(movie_id):
    cur = mysql.connection.cursor()
    query = f"select c.FullName , c.image , c.ID , mc.role from moviecast mc , castmember c WHERE c.ID=mc.castID  AND mc.movieID = {movie_id};"
    cur.execute(query)
    data = cur.fetchall()
    query = f"select m.MovieName from movie m where m.ID={movie_id}"
    cur.execute(query)
    name = cur.fetchall()
    return render_template("movieCast.html", data=data, name=name)


@app.route('/cast')
def casts():
    cur = mysql.connection.cursor()
    query = "select * from castmember ;"
    cur.execute(query)
    data = cur.fetchall()
    return render_template("casts.html", data=data)


@app.route('/cast/<int:cast_id>')
def cast(cast_id):
    cur = mysql.connection.cursor()
    query = f"select * from castmember WHERE ID={cast_id};"
    cur.execute(query)
    data = cur.fetchall()
    return render_template("cast.html", data=data)


@app.route('/genres')
def Genres():
    cur = mysql.connection.cursor()
    query = "SELECT DISTINCT(Genre) FROM moviegenre;"
    cur.execute(query)
    data = cur.fetchall()
    return render_template("genres.html", data=data)


@app.route('/genres/<movieGenre>')
def get_movies_genre(movieGenre):
    cur = mysql.connection.cursor()
    query = f'''SELECT m.ID, m.MovieName, g.Genre FROM movie m,moviegenre g WHERE g.Genre = "{movieGenre}" AND g.movieID = m.ID;'''
    cur.execute(query)
    data = cur.fetchall()
    return render_template("genre.html", data=data, movieGenre=movieGenre)


@app.route('/cast/<int:cast_id>/movies')
def get_cast_movies(cast_id):
    cur = mysql.connection.cursor()
    query = f'''SELECT m.ID, m.MovieName, mc.role FROM movie m, castmember c, moviecast mc 
                WHERE c.ID={cast_id} AND mc.castID=c.ID AND m.ID=mc.movieID'''
    cur.execute(query)
    data = cur.fetchall()
    query = f'''select c.FullName, c.image FROM castmember c WHERE c.ID={cast_id}'''
    cur.execute(query)
    cast = cur.fetchall()
    return render_template("castwork.html", data=data, cast=cast)


@app.route('/top10movies')
def get_top_10():
    cur = mysql.connection.cursor()
    query = "SELECT m.MovieName , m.ID ,m.poster, m.TotalRevenue from movie m ORDER BY TotalRevenue DESC LIMIT 10"
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        row['TotalRevenue'] = float(row['TotalRevenue'])
    return render_template("topMovie.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)