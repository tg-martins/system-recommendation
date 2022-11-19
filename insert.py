from neo4j import GraphDatabase
import pandas as pd

url = 'bolt://localhost:7687'
usuario = "neo4j"
senha = '123'

nrows = 2000


class Movie:
    def __init__(self, id, title, genres, rating):
        self.id = id
        self.title = title
        self.genres = genres
        self.rating = rating

    def __str__(self):
        return '{' + f'id: "{self.id}", title: "{self.title}", genres: {self.genres}, rating: {self.rating}' + '}'


class Principal:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __str__(self):
        return '{' + f'id: "{self.id}", name: "{self.name}"' + '}'


class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_movies(self):
        with self.driver.session() as session:
            session.execute_write(self._remove_data)
            session.execute_write(self._create_movies)

    @staticmethod
    def _remove_data(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def _create_movies(tx):
        df_movies = pd.read_table('datasets/title.basics.tsv', nrows=nrows)
        df_movie_ratings = pd.read_table('datasets/title.ratings.tsv')
        df_name_principals = pd.read_table('datasets/name.basics.tsv')
        df_principals = pd.read_table('datasets/title.principals.tsv', nrows=nrows)
        df_movies_id = df_principals.drop_duplicates(subset=['nconst'])['nconst']
        df_principal_names = df_name_principals[df_name_principals['nconst'].isin(df_movies_id)]

        inserts = []

        for _, row_principal in df_principal_names.iterrows():
            principal = Principal(row_principal['nconst'], row_principal['primaryName'], '')

            inserts.append(f"CREATE ({principal.id}: person {principal})")

        for _, row_movie in df_movies.iterrows():
            df_movie_rating = df_movie_ratings[(df_movie_ratings['tconst'] == row_movie['tconst'])]

            movie = Movie(row_movie['tconst'], row_movie['primaryTitle'], row_movie['genres'].split(','), 0)

            if len(df_movie_rating['averageRating'].values) > 0:
                movie.rating = df_movie_rating['averageRating'].values[0]

            inserts.append(f"CREATE ({movie.id}: movie {movie})")

            df_movie_principals = df_principals[(df_principals['tconst'] == row_movie['tconst'])]

            for _, row_principal in df_movie_principals.iterrows():
                movie_principal = Principal(row_principal['nconst'], _, row_principal['category'])

                inserts.append(f"CREATE ({movie_principal.id})-[:{movie_principal.category}]->({movie.id})")

        tx.run('\n'.join(inserts))


if __name__ == "__main__":
    db = App(url, usuario, senha)

    try:
        db.create_movies()
        print("Filmes carregados")
    finally:
        db.close()
