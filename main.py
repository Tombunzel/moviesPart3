import argparse
import sys
from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson

# Initialize the parser
parser = argparse.ArgumentParser(description="Run MovieApp with specified storage file.")

# Add argument for the input file
parser.add_argument('file_name', type=str, help='The input file (must be .json or .csv)')

# Parse the arguments
args = parser.parse_args()

# Extract the file name from the parsed arguments
file_name = args.file_name
extension = file_name.split('.')[-1]

# Logic for handling different file extensions
if extension == 'json':
    storage = StorageJson(file_name)
elif extension == 'csv':
    storage = StorageCsv(file_name)
else:
    print("Unsupported file extension")
    sys.exit()

# Create and run the MovieApp
movie_app = MovieApp(storage)
movie_app.run()
