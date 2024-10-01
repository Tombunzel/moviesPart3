from abc import ABC, abstractmethod


class IStorage(ABC):
    """class of storage interface"""

    @abstractmethod
    def list_movies(self):
        """list all movies in storage"""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster_url, imdb_url, flag_urls, user_note):
        """add movie to storage"""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """delete movie from storage"""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """update movie in storage"""
        pass
