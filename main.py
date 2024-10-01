from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson

storage = StorageJson('data.json')
# storage = StorageCsv('lilach.csv')
# storage = StorageJson('tom.json')
movie_app = MovieApp(storage)
movie_app.run()
