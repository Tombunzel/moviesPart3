from istorage import IStorage


class StorageCsv(IStorage):
    """Class to handle csv data"""
    def __init__(self, file_path):
        """constructor"""
        self.file_path = file_path

    def save_movies(self, new_movies):
        """
        Gets movies as an argument and saves them to the csv file.
        """
        with open(f'data/{self.file_path}', "w", encoding="UTF-8") as fileobj:
            output = 'title,year,rating,poster_url,imdb_url,flag_url,user_note\n'
            for movie, infos in new_movies.items():
                output += (f'{movie},{infos["year"]},{infos["rating"]},{infos["poster_url"]},'
                           f'{infos["imdb_url"]},{infos["flag_url"]},{infos["user_note"]}\n')
            fileobj.write(output)

    def get_movies(self):
        """gets movies from the csv file, if the file doesn't exist, it creates a new one
        returns the movies in the csv file"""
        try:
            with open(f'data/{self.file_path}', "r", encoding="UTF-8") as fileobj:
                movies = {}
                next(fileobj)  # skipping the first line of headers in the csv file
                for line in fileobj:
                    fields = line.strip().split(',')
                    movies[fields[0]] = {"year": int(fields[1]),
                                         "rating": float(fields[2]),
                                         "poster_url": fields[3],
                                         "imdb_url": fields[4],
                                         "flag_url": fields[5],
                                         "user_note": fields[6],
                                         }
                return movies
        except FileNotFoundError:
            with open(f'data/{self.file_path}', "w", encoding="UTF-8") as fileobj:
                movies = 'title,rating,year,poster_url,imdb_url,flag_url,user_note\n'
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
        Adds a movie to the movie database
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
        Updates a movie from the movie database
        """
        movies = self.get_movies()
        movies[title]['user_note'] = user_note
        self.save_movies(movies)
