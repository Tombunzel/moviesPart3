from storage.istorage import IStorage
import json


class StorageJson(IStorage):
    """Class to handle json data"""
    def __init__(self, file_path):
        """constructor"""
        self.file_path = file_path

    def save_movies(self, new_movies):
        """
        Gets movies as an argument and saves them to the JSON file.
        """
        with open(f'data/{self.file_path}', "w", encoding="UTF-8") as fileobj:
            json_str = json.dumps(new_movies, indent=4)
            fileobj.write(json_str)

    def get_movies(self):
        """gets movies from the json file, if the file doesn't exist, it creates a new one
        returns the movies in the json file"""
        try:
            with open(f'data/{self.file_path}', "r", encoding="UTF-8") as fileobj:
                json_str = fileobj.read()
                movies = json.loads(json_str)
                return movies
        except FileNotFoundError:
            with open(f'data/{self.file_path}', "w", encoding="UTF-8") as fileobj:
                movies = '{}'
                fileobj.write(movies)
                print(f"\n\033[33mCreated new file '{self.file_path}'\033[00m")
                return {}

    def list_movies(self):
        """list all movies in data"""
        movies = self.get_movies()
        for movie, infos in movies.items():
            print(f"{movie} ({infos['year']}): {infos['rating']}")

    def add_movie(self, title, year, rating, poster_url, imdb_url, flag_urls, user_note):
        """
        Adds a movie to the movie database.
        """
        movies = self.get_movies()
        movies[title] = {"rating": rating, "year": year, "poster_url": poster_url,
                         "imdb_url": imdb_url, "flag_url": flag_urls, "user_note": user_note}
        self.save_movies(movies)

    def delete_movie(self, title):
        """delete movie from data"""
        movies = self.get_movies()
        del movies[title]
        self.save_movies(movies)

    def update_movie(self, title, user_note):
        """
        Updates a movie from the movie database.
        """
        movies = self.get_movies()
        movies[title]['user_note'] = user_note
        self.save_movies(movies)
