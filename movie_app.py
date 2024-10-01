import difflib
import random
import sys
import requests
import data_fetcher


class MovieApp:
    """class of movie app"""
    def __init__(self, storage):
        """constructor"""
        self._storage = storage

    def get_list_of_ratings(self):
        """
        create list of all movie ratings
        :return: list of all ratings
        """
        list_of_ratings = []
        for _, infos in self._storage.get_movies().items():
            list_of_ratings.append(infos['rating'])
        return list_of_ratings

    @staticmethod
    def print_menu_get_choice():
        """
        print all menu options and get user choice
        :return: returns user's choice
        """
        print("\033[33mMenu:\n"
              "0. Exit\n"
              "1. List movies\n"
              "2. Add movie\n"
              "3. Delete movie\n"
              "4. Update movie\n"
              "5. Stats\n"
              "6. Random movie\n"
              "7. Search movie\n"
              "8. Movies sorted by rating\n"
              "9. Movies sorted by year\n"
              "10. Filter movies\n"
              "11. Generate website\n")
        user_input = input("\033[00mEnter choice (0-11): \033[32m")
        print("\033[00m", end='')  # white
        return user_input

    def _command_list_movies(self):
        """
        prints all movies in data
        """
        movies = self._storage.get_movies()
        print(f"\n{len(movies)} movies in total:")
        for movie, infos in movies.items():
            print(f"  {movie} ({infos['year']}): {infos['rating']}")

    def _command_add_movie(self):
        """
        uses the data_fetcher file to search and fetch a dict of info about a movie
        from the api, and then writes the info to the json file.
        """
        while True:
            movie_name = input("\nEnter new movie name: \033[32m")
            if not movie_name:
                print("\n\033[31mNothing entered, sending you back to main menu\033[00m")
                break

            try:
                movie_dict = data_fetcher.fetch_api_movie_dict(movie_name)
                if movie_dict['Type'] != 'movie':
                    print(f"\n\033[31mCouldn't find a movie called {movie_name}\033[00m")
                    break
                title = movie_dict['Title']
                year = int(movie_dict['Year'])
                user_input = input(f"\033[00m\nThe following insert was found:"
                                   f"'\033[32m{title} ({year})\033[00m'.\n\n"
                                   f"Confirm? (y/n) \033[32m")
                print('\033[00m', end='')
            except KeyError:
                print("\033[31m\nCouldn't find movie\033[00m")
                continue
            except requests.exceptions.ConnectionError:
                print("\033[31m\nConnection error, please check your connection.\033[00m")
                break

            if user_input.lower() == 'y':
                if movie_dict['Type'] != 'movie':
                    print(f"\n\033[31m{title} is not a movie, but a {movie_dict['Type']}\033[00m")
                    break

                rating = float(movie_dict['Ratings'][0]['Value'].split('/')[0])
                poster_url = movie_dict['Poster']
                imdb_template = 'https://www.imdb.com/title/'
                movie_imdb_id = movie_dict['imdbID']
                imdb_url = imdb_template + movie_imdb_id
                country = movie_dict['Country'].split(',')[0]
                flag_urls = data_fetcher.fetch_country_flag_url(country)
                self._storage.add_movie(title, year, rating, poster_url, imdb_url, flag_urls, user_note='')
                print(f"\033[00m\nMovie {title} successfully added")
                break

            elif user_input.lower() == 'n':
                ask_quit = input("\ntype c to cancel or enter to try again: ")
                if ask_quit.lower() == 'c':
                    break

            else:
                print("\033[31m\nSorry, I didn't get that, please try again. \033[00m")

    def _command_delete_movie(self):
        """
        removes a movie from data according to user's input
        :return: -
        """
        movies = self._storage.get_movies()
        while True:
            name = input("\nEnter movie name to delete: \033[32m")
            if not name:
                print("\n\033[31mNothing entered, sending you back to main menu\033[00m")
                break
            print("\033[00m")  # white
            if name not in movies:
                print(f"\033[31mCouldn't find movie {name}\033[00m")
            else:
                self._storage.delete_movie(name)
                print(f"Movie {name} successfully deleted")
                break

    def _command_update_movie(self):
        """
        Allows user to insert a note to a movie in data
        movie_titles_lower is a dict of lowercase titles referring to the correct titles
        """
        movies = self._storage.get_movies()
        while True:
            name = input("\033[00mEnter movie name: \033[32m")
            print("\033[00m", end='')  # white
            if not name:
                print("\n\033[31mNothing entered, sending you back to main menu\033[00m")
                break
            movie_titles_lower = {movie.lower(): movie for movie in movies}
            if name.lower() not in movie_titles_lower:
                print(f"\n\033[31mCouldn't find movie {name}!\033[00m")
                break

            correct_movie_title = movie_titles_lower[name.lower()]
            user_note = input("Enter movie notes: ")
            self._storage.update_movie(correct_movie_title, user_note)
            print(f"\n\033[00mMovie {correct_movie_title} successfully updated")
            break

    @staticmethod
    def calc_avg_rating(list_of_ratings):
        """
        calculates the average rating from the list of all movie ratings
        :return: the average rating
        """
        sum_ratings = 0
        amount_of_movies = len(list_of_ratings)
        for rating in list_of_ratings:  # iterate over all rating values in dict
            sum_ratings += rating  # increment to sum_ratings
        average_rating = sum_ratings / amount_of_movies  # calculate average
        return average_rating

    @staticmethod
    def calc_median_rating(movies, list_of_ratings):
        """
        calculates median rating depending on amount of movies (odd or even)
        :return: the median rating
        """
        list_of_ratings = sorted(list_of_ratings, reverse=True)
        movies_length = len(movies)
        if movies_length % 2 == 0:  # if even number of movies
            left_median = list_of_ratings[int(movies_length / 2) - 1]  # get "left median"
            right_median = list_of_ratings[int(movies_length / 2)]  # get "right median"
            median = (left_median + right_median) / 2  # calculate average of both
            return median
        median = list_of_ratings[int(len(movies) / 2)]  # get rating in middle of list
        return round(median, 1)

    @staticmethod
    def get_best_movie(movies):
        """
        fetches movie with the highest rating
        :param movies: dict of movies
        :return: movie name, its year and its rating
        """
        highest_rating = 0
        best_movie = ''
        year = 0
        for movie, infos in movies.items():  # go over keys and values in dict
            rating = infos['rating']
            if rating > highest_rating:  # find the next high rating
                year = infos['year']
                highest_rating = rating  # assign rating value
                best_movie = movie  # assign movie name

        return best_movie, year, highest_rating

    @staticmethod
    def get_worst_movie(movies):
        """
        fetches movie with the lowest rating
        :param movies: dictionary of movies
        :return: movie name, its year and its rating
        """
        lowest_rating = 11  # all ratings will be smaller when compared
        worst_movie = ''
        year = 0
        for movie, infos in movies.items():  # iterate over movies and ratings in dict
            rating = infos['rating']
            if rating < lowest_rating:  # find next lower rating
                year = infos['year']
                lowest_rating = rating  # assign rating value
                worst_movie = movie  # assign movie name

        return worst_movie, year, lowest_rating

    def _command_stats(self):
        """
        use different functions to fetch and print different movies stats
        :return: -
        """
        movies = self._storage.get_movies()
        if not movies:
            print("No movies in the database yet")
        else:
            list_of_ratings = self.get_list_of_ratings()
            best_movie, best_year, highest_rating = self.get_best_movie(movies)
            worst_movie, worst_year, lowest_rating = self.get_worst_movie(movies)
            median = self.calc_median_rating(movies, list_of_ratings)
            average_rating = round(self.calc_avg_rating(list_of_ratings), 1)

            print(f"\nAverage rating: {average_rating}")
            print(f"Median rating: {median}")
            print(f"Best movie: {best_movie} ({best_year}), {highest_rating}")
            print(f"Worst movie: {worst_movie} ({worst_year}), {lowest_rating}")

    def _command_random_movie(self):
        """
        print a random movie from data
        :return: -
        """
        movies = self._storage.get_movies()
        if not movies:
            print("No movies in the database yet")
        else:
            movie, infos = random.choice(list(movies.items()))  # assign random tuple of movie,rating
            print(f"\nYour movie for tonight:\n"
                  f"{movie} ({infos['year']}), it's rated: {infos['rating']}")

    def _command_search_movie(self):
        """
        allow user to search for a movie in the dictionary
        :return: -
        """
        movies = self._storage.get_movies()
        while True:
            search_query = input("\nEnter part of movie name: \033[32m")
            if not search_query:
                print("\n\033[31mNothing entered, sending you back to main menu\033[00m")
                break
            print("\033[00m")  # white
            list_of_matches = difflib.get_close_matches(search_query.lower(),
                                                        list(movies.keys()), cutoff=0.4)
            if not list_of_matches:
                print("\033[31mSorry, couldn't find movie.\033[00m")
                break

            for match in list_of_matches:
                print(f"{match} ({movies[match]['year']}): {movies[match]['rating']}")

            break

    def _command_movies_by_rating(self):
        """
        print all movies from dict in descending rating order
        """
        movies = self._storage.get_movies()
        list_of_ratings = self.get_list_of_ratings()
        print()
        list_of_ratings = sorted(list(set(list_of_ratings)), reverse=True)  # no duplicates, descending
        for rating_in_list in list_of_ratings:
            for movie, infos in movies.items():
                rating = infos['rating']
                if rating_in_list == rating:  # find matching ratings from list in dict
                    print(f"{movie} ({infos['year']}), {rating}")  # print matching name and rating

    def _command_movies_by_year(self):
        """
        prints all movies ordered by year of publish, order chosen by user
        """
        movies = self._storage.get_movies()
        list_of_years = []

        while True:
            user_input = input("\nMost recent or old first? (r/o) \033[32m")
            print("\033[00m", end="")
            user_input = user_input.lower()
            if user_input.lower() == "r":
                is_reverse = True
                break
            if user_input.lower() == "o":
                is_reverse = False
                break
            print("\033[31m\nPlease enter either 'a' for ascending or 'd' for descending\033[00m")

        for info in movies.values():
            list_of_years.append(info['year'])

        list_of_years = sorted(list(set(list_of_years)), reverse=is_reverse)

        for year in list_of_years:
            for movie, info in movies.items():
                if info['year'] == year:
                    print(f"{movie} ({info['year']}): {info['rating']}")

    @staticmethod
    def check_filter_input(user_input):
        """
        Check that user input has a valid numerical value
        :param user_input: user input
        :return: user_input as int
        """
        try:
            user_input = int(user_input)
            return user_input
        except (ValueError, TypeError):
            print("\033[31m\nPlease enter a number or leave blank for no filter\033[00m\n")
            return user_input

    def _command_filter_movies(self):
        """
        allows user to print movies filtered by min rating and range of years
        """
        movies = self._storage.get_movies()
        while True:
            minimum_rating = input("\nEnter minimum rating "
                                   "(leave blank for no minimum rating): \033[32m")
            print("\033[00m", end="")
            if minimum_rating == '':
                minimum_rating = 0
            try:
                minimum_rating = float(minimum_rating)
                if 0 <= minimum_rating <= 10:
                    break
                print("\033[31m\nPlease enter a number between 0 and 10\033[00m")
            except ValueError:
                print("\033[31m\nPlease enter a number or leave blank for no filter\033[00m")

        while True:
            start_year = input("Enter start year (leave blank for no start year): \033[32m")
            print("\033[00m", end="")
            if start_year == '':
                start_year = 1888

            start_year = self.check_filter_input(start_year)

            if isinstance(start_year, int):
                break

        while True:
            end_year = input("Enter end year (leave blank for no end year): \033[32m")
            print("\033[00m", end="")
            if end_year == '':
                end_year = 2024
                break
            end_year = self.check_filter_input(end_year)
            if isinstance(end_year, int):
                break

        print("\nFiltered movies:")
        for movie, info in movies.items():
            if info['rating'] >= minimum_rating and start_year <= info['year'] <= end_year:
                print(f"  {movie} ({info['year']}): {info['rating']}")

    @staticmethod
    def _read_template():
        """reads the template html file and returns its contents"""
        with open("_static/index_template.html", "r", encoding="UTF-8") as handle:
            template = handle.read()
            return template

    def _create_html(self, template):
        """creates a new html file using the template and a dict of all movies"""
        movies = self._storage.get_movies()
        site_title = "My Movies Site"
        with open("_static/index.html", "w", encoding="UTF-8") as handle:
            output = template
            output = output.replace("__TEMPLATE_TITLE__", site_title)
            for movie in movies.keys():
                poster = movies[movie]['poster_url']
                imdb = movies[movie]['imdb_url']
                try:
                    flag_url = movies[movie]['flag_url']
                except KeyError:
                    flag_url = ''
                title = movie
                year = movies[movie]['year']
                rating = movies[movie]['rating']
                note = movies[movie]['user_note']
                new_movie_grid = (f'        <li>\n'
                                  f'<div class="movie">\n'
                                  f'<a href="{imdb}" target="_blank">\n'
                                  f'<img class="movie-poster" src="{poster}" title="{note}"/>\n'
                                  f'</a>\n'
                                  f'<div class="movie-title">{title}</div>\n'
                                  f'<div class="movie-year">{year}</div>\n'
                                  f'<img class="flag-icon" src="{flag_url}">\n'
                                  f'<div class="movie-rating">{rating}/10</div>\n'
                                  f'</div>\n'
                                  f'</li>\n')
                output += '        __TEMPLATE_MOVIE_GRID__\n'
                output = output.replace("__TEMPLATE_MOVIE_GRID__", new_movie_grid)
            output += '    </ol>'
            output += '</div>'
            output += '</body>\n</html>'
            handle.write(output)

    def _generate_web(self):
        """generates the new web page by using the different functions"""
        template = self._read_template()
        self._create_html(template)
        print("\nWebsite was generated successfully.")

    def _command_generate_website(self):
        """generates an HTML file to view all movies from the data"""
        if not self._storage.get_movies():
            print("No movies in the database yet")
        else:
            self._generate_web()

    @staticmethod
    def exit_program():
        """exits the program"""
        print("Bye!")
        sys.exit()

    def run(self):
        """
        main function to run the CLI
        """
        print()
        print("********** My Movies Database **********")
        while True:
            menu_options = [
                self.exit_program,
                self._command_list_movies,
                self._command_add_movie,
                self._command_delete_movie,
                self._command_update_movie,
                self._command_stats,
                self._command_random_movie,
                self._command_search_movie,
                self._command_movies_by_rating,
                self._command_movies_by_year,
                self._command_filter_movies,
                self._command_generate_website
            ]

            user_input = self.print_menu_get_choice()

            try:
                user_input = int(user_input)
            except (TypeError, IndexError, ValueError):
                print("\033[31m\nInvalid choice\033[00m")
                input("\nPress enter to continue \033[00m")
                continue

            menu_options[user_input]()
            input("\nPress enter to continue \033[00m")
