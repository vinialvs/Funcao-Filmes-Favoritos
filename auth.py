import tmdbsimple as tmdb


#MÉTODO DE PESQUISA DE FILMES.
class TMDBClient:
    def __init__(self, api_key):
        tmdb.API_KEY = api_key
        self.search = tmdb.Search()

    def search_movie(self, query):
        return self.search.movie(query=query)['results']