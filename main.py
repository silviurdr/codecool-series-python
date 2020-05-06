from flask import Flask, render_template, url_for, redirect, request, session, flash
from data import queries

app = Flask('codecool_series')

app.secret_key = "safa55999$($)#*$&$&&&"


@app.route('/')
def index():
    shows = queries.get_shows()

    if 'username' in session:
        username = session['username']
        return render_template('index.html', shows=shows, username=username)

    return render_template('index.html', shows=shows)


@app.route('/top-rated-shows')
def top_rated_shows():

    top_rated_shows_dict = queries.get_top_rated_shows()
    for show in top_rated_shows_dict:
        genres = ""
        show_genres = queries.get_genres_for_shows(show['id'])
        for genre in show_genres:
            genres += genre['name'] + ", "
        show['genres'] = genres[:-2]
    if 'username' in session:
        username = session['username']

        return render_template('top-rated-shows.html', top_rated_shows=top_rated_shows_dict, username=username)

    return render_template('top-rated-shows.html', top_rated_shows=top_rated_shows_dict)


@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        queries.add_new_user_to_database(username, password)

        return redirect(url_for('top_rated_shows'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form['username']
        database_password = queries.get_password_for_user(request.form['username'])
        if database_password:

            session['username'] = username
            return redirect(url_for('top_rated_shows'))

        else:
            return redirect(url_for('top_rated_shows'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('show_id', None)
    return redirect('/')


@app.route('/top-20-actors')
def top_20_actors():

    top_actors = queries.top_20_actors()
    return render_template('top-20-actors.html', top_actors=top_actors)


@app.route('/add-favorite/<show_id>')
def add_favorite(show_id):

    fav_username = session['username']
    fav_show_id = show_id
    queries.add_favorite_to_user(fav_username, fav_show_id)
    
    return redirect(url_for('top_rated_shows'))

@app.route('/user-page')
def user_page():

    username = session['username']
    favorites = queries.get_favorites_for_user(username)
    return render_template('user-page.html', favorites=favorites, username=username)


@app.route('/show-details/<show_id>')
def show_details(show_id):

    username = session['username']
    show_id = int(show_id)
    show_info = queries.get_show_info_by_show_id(show_id)[0]
    genres = queries.get_genres_for_shows(show_id)
    show_genres = ""
    for genre in genres:
        show_genres += (genre['name']) + ', '
    show_info['genres'] = show_genres[:-2]

    comments = queries.get_comments_for_show(show_id)
    if comments:
        return render_template('show-details.html', show_info=show_info, username=username, comments=comments)

    return render_template('show-details.html', show_info=show_info, username=username)


@app.route('/add-comment/<show_id>', methods=["GET", 'POST'])
def add_comment(show_id):

    session['show_id'] = show_id

    if request.method == "POST":
        data = {}
        data['username'] = session['username']
        data['show_id'] = session['show_id']
        data['subject'] = request.form['subject']
        data['comment'] = request.form['comment']
        queries.add_comment_to_database(data)
        return redirect(url_for('show_details', show_id=show_id))

    return render_template('new-comment.html')


@app.route('/shows-by-genre/<genre>')
def shows_by_genre(genre):

    top_rated_movies_genre = queries.get_rated_shows_genre(genre)
    print(top_rated_movies_genre)
    return render_template('popular-shows-genre.html', top_rated_movies_genre=top_rated_movies_genre)



@app.route('/design')
def design():

    return render_template('design.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
