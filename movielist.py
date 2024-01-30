import sqlite3
import pandas as pd
from tabulate import tabulate
from fuzzywuzzy import fuzz

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