import sqlite3
import tmdbsimple as tmdb
import time
import pandas as pd
from tabulate import tabulate
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import os

#CHAMANDO A API.
load_dotenv(".env")
API_KEY: str = os.getenv('API_KEY')

#MÉTODO DE PESQUISA DE FILMES.
class TMDBClient:
    def __init__(self, api_key):
        tmdb.API_KEY = api_key
        self.search = tmdb.Search()

    def search_movie(self, query):
        return self.search.movie(query=query)['results']

#LISTA DE FAVORITOS.
class MovieList:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    release_date TEXT,
                    original_language TEXT
                )
            ''')

    def view_table(self):
        with sqlite3.connect (self.db_path) as conn:
            query = 'SELECT * FROM movies'
            df = pd.read_sql_query(query, conn) 
            df = df.drop(columns=['id'], errors='ignore')
            df = df.rename(columns={'title' : 'Titulo', 'release_date' : 'Data de Lançamento', 'original_language' : 'Idioma'}, errors='ignore')
            df['Data de Lançamento'] = pd.to_datetime (df['Data de Lançamento'])
            df['Data de Lançamento'] = df['Data de Lançamento'].dt.strftime('%d/%m/%Y')
            df['Idioma'] = df['Idioma'].str.capitalize()
            tabela = (tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            return tabela


    def add_movie(self, title, release_date, original_language):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM movies WHERE title = ?', (title,))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute('INSERT INTO movies (title, release_date, original_language) VALUES (?, ?, ?)',
                                (title, release_date, original_language))
                
                print(f'O filme "{title}" foi adicionado à lista.')
            else:
                print(f'O filme "{title}" já está na lista.')

    def get_movies(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT title, release_date, original_language FROM movies')
            return cursor.fetchall()

    def delete_movie(self, movie):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM movies WHERE title = ?', 
                           (movie, ))

    def remover_titulo_aproximado(self, movie):
        melhor_correspondencia = None
        melhor_pontuacao = 0 

        for filme in self.get_movies():
            pontuacao = fuzz.ratio(movie, filme[0])
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_correspondencia = filme[0]

        return melhor_correspondencia

#INTERFACE PRINCIPAL
def main():
    api_key = API_KEY
    tmdb_client = TMDBClient(api_key)
    movie_list = MovieList()

    escolha = '0' 
    while escolha != '4':

        print ('-- SUA LISTA DE FAVORITOS -- \n')
        time.sleep(0.5)
        print (' [1] Adicionar filme na lista.\n', 
            '[2] Remover filme da lista.\n', 
            '[3] Ver lista.\n'
            ' [4] Encerrar o programa. \n')

        escolha = (input(str('O que deseja fazer? ')))
        if escolha == '1':

            while True:
                user_input = input('Qual o filme que você deseja procurar? ')
                search_results = tmdb_client.search_movie(query=user_input)

                for result in search_results:
                    print(result['title'])
                    user_checkin = input('Este é o filme que você procurou? (S/N) ')

                    if 'S' in user_checkin.upper():
                        movie_list.add_movie(result['title'], result['release_date'], result['original_language'])
                        print(movie_list.view_table())
                        break

                user_checkin2 = input('Deseja procurar outro filme? (S/N) ')

                if 'N' in user_checkin2.upper():
                    break
            
        elif escolha == '2':
        
            print (movie_list.view_table())
            user_input = input('Qual o filme que você deseja remover da lista? ')
            user_input = movie_list.remover_titulo_aproximado(user_input)
            movie_list.delete_movie(user_input)
            print (movie_list.view_table())
        

        elif escolha == '3':
            print (movie_list.view_table())
        
        elif escolha == '4':
            print ('Encerrando o programa.')
            break

if __name__ == "__main__":
    main()
