from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

# storage = StorageJson('storage/movies.json')
# storage = StorageCsv('storage/mary.csv')
storage = StorageJson('storage/tom.json')
movie_app = MovieApp(storage)
movie_app.run()
