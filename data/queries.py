from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_top_rated_shows():
    return data_manager.execute_select('SELECT id, title, year, runtime, ROUND(rating, 2) as rating, trailer, homepage, overview FROM shows ORDER BY rating DESC LIMIT 15')


def get_genres_for_shows(show_id):
    return data_manager.execute_select(f'SELECT genres.name from genres INNER JOIN show_genres on show_genres.genre_id=genres.id WHERE show_genres.show_id={show_id} LIMIT 3')


def add_new_user_to_database(new_username, new_password):

    return data_manager.execute_dml_statement(f"INSERT INTO users (username, password) VALUES ('{new_username}', '{new_password}')")


def get_password_for_user(username):
    return data_manager.execute_select(f'''SELECT password from users where username='{username}';''')


def top_20_actors():
    return data_manager.execute_select(f"""SELECT a.name, string_agg(title, ', ') actor_shows, COUNT(*) as shows_number from actors a
                                            INNER JOIN show_characters sc ON a.id=sc.actor_id
                                            INNER JOIN shows s on sc.show_id=s.id
                                            GROUP by a.name
                                            ORDER BY shows_number DESC
                                            LIMIT 20""")


def add_favorite_to_user(fav_username, fav_show_id):
    return data_manager.execute_dml_statement(f"""INSERT INTO favorites (username, show_id) VALUES ('{fav_username}', '{fav_show_id}')""")


def get_favorites_for_user(username):
    return data_manager.execute_select(f"""SELECT DISTINCT title from shows INNER JOIN favorites ON shows.id=favorites.show_id 
                                        INNER JOIN users on favorites.username=users.username WHERE users.username='{username}'; """)
                                        

def get_show_info_by_show_id(show_id):
    return data_manager.execute_select(f"""SELECT id, title, runtime, year, overview FROM shows WHERE shows.id={show_id};
                                    """)


def add_comment_to_database(data):
    return data_manager.execute_dml_statement(""" INSERT INTO comments (username, show_id, subject, comment) VALUES( %(data_username)s, %(data_show_id)s, %(data_subject)s, %(data_comment)s)
                                    """, {'data_username': data['username'], 'data_show_id': data['show_id'], 'data_subject': data['subject'], 'data_comment': data['comment']})


def get_comments_for_show(show_id):
    return data_manager.execute_select(f"""SELECT subject, comment from comments WHERE show_id={show_id}""")


def get_rated_shows_genre(genre):
    return data_manager.execute_select(f"""SELECT title, shows.id from shows JOIN show_genres ON shows.id=show_genres.show_id JOIN genres ON show_genres.genre_id=genres.id WHERE genres.name='{genre}' ORDER by shows.rating DESC LIMIT 10;""")