from neo4j import GraphDatabase

url = 'bolt://localhost:7687'
usuario = "neo4j"
senha = '123'


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


conn = Neo4jConnection(uri=url,
                       user=usuario,
                       pwd=senha)


def search_recommendations(movie):
    query_search_persons_movie = """
           MATCH (person:person)-[*]->(movie:movie {id: '""" + movie['movie.id'] + """'})
           RETURN person.id, person.name
       """

    persons_movie = []

    for person in conn.query(query_search_persons_movie):
        persons_movie.append(dict(person))

    persons_query = " OR ".join(
        map(lambda person: "(:person {id: '" + person['person.id'] + "'})-[*]->(movie)", persons_movie))

    query_search_recommendations = """
        MATCH (movie:movie) 
        WHERE 
            ANY (genre IN """ + str(movie['movie.genres']) + """ WHERE genre IN movie.genres) 
            AND (""" + str(persons_query) + """)
            OR movie.rating >= """ + str(movie['movie.rating']) + """
        RETURN movie.id, movie.title, movie.genres, movie.rating
        ORDER BY movie.rating DESC
        LIMIT 5
    """

    return conn.query(query_search_recommendations)


def search_movie(id):
    query_search_movie = """
        MATCH (movie:movie {id: '""" + id + """'})
        RETURN movie.id, movie.title, movie.genres, movie.rating
    """

    return conn.query(query_search_movie)


if __name__ == "__main__":
    id_movie = input('Informe o id do filme: ')

    query_result_search_movie = search_movie(id_movie)

    if len(query_result_search_movie) > 0:
        movie = dict(query_result_search_movie[0])

        print("\nFilme escolhido:\n")

        print(movie)

        print("\nRecomendações:\n")

        recommendations = search_recommendations(dict(query_result_search_movie[0]))

        for recommendation in recommendations:
            print(dict(recommendation))
    else:
        print('Filme não encontrado')
