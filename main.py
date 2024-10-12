import argparse
import sys
from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


def initialize_parser():
    """initialize the parser with file_name argument"""
    parser = argparse.ArgumentParser(description="Run MovieApp with specified storage file.")
    parser.add_argument('file_name', type=str, help='The input file (must be .json or .csv)')
    return parser


def get_file_name_and_extension(parser):
    """get the file extension from the parser"""
    args = parser.parse_args()
    file_name = args.file_name
    extension = file_name.split('.')[-1]
    return file_name, extension


def main():
    """runs the MovieApp with different file types
    """
    parser = initialize_parser()
    file_name, extension = get_file_name_and_extension(parser)
    if extension == 'json':
        storage = StorageJson(file_name)
    elif extension == 'csv':
        storage = StorageCsv(file_name)
    else:
        print("Unsupported file extension")
        sys.exit()

    # Instantiate and run the MovieApp
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
