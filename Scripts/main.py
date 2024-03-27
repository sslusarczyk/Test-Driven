from flask import Flask, render_template, request, url_for, flash, redirect
import tmdb_client
import random
import datetime

def create_app(): # dodane do publikacji waitress
    app = Flask(__name__)
    FAVORITES = set() # dodane do publikacji waitress
    app.secret_key = b'secret' # dodane do publikacji waitress
    return app # dodane do publikacji waitress

app = create_app()  # Wywołanie funkcji create_app() i przypisanie wyniku do zmiennej app # dodane do publikacji waitress


@app.route('/')
#def homepage():
 #   available_lists = ['popular', 'top_rated', 'upcoming', 'now_playing'] 
  #  selected_list = request.args.get('list_type', 'popular')
   # if selected_list not in available_lists:
    #    return redirect(url_for('homepage', list_type='popular'))
    #movies = tmdb_client.get_movies(how_many=20, list_type=selected_list)
    #return render_template("homepage.html",available_lists=available_lists, movies=movies, current_list=selected_list)

@app.route('/')
def index():
    # Get the value of 'list_type' parameter from the query string
    list_type = request.args.get('list_type', 'popular')
    
    # Call the tmdb_client.call_tmdb_api function with the appropriate argument
    movies = tmdb_client.call_tmdb_api(f'movie/{list_type}')
    
    # Render the template with the retrieved movies data
    return render_template('index.html', movies=movies)
    
    

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}
        
@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])['file_path']
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)
    
@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)

@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)

@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))
    
@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies)
    

    
if __name__ == '__main__':
    app = create_app() # dodane do publikacji waitress
    app.run(debug=True)
    