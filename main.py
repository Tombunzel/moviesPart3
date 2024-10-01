from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson

# storage = StorageJson('movies.json')
# storage = StorageCsv('mary.csv')
storage = StorageJson('tom.json')
movie_app = MovieApp(storage)
movie_app.run()
