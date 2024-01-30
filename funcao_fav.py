from movielist import MovieList
from auth import TMDBClient
import time
from dotenv import load_dotenv
import os

#CHAMANDO A API.
load_dotenv(".env")
API_KEY: str = os.getenv('API_KEY')


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
