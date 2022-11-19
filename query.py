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


def search(query):
    for line in conn.query(query):
        print(dict(line))


if __name__ == "__main__":
    print("Filmes que Charles Kayser e John Ott aparecem juntos mas que não atua a Drew Barrymore.:\n")

    search("""
        MATCH (p1:person {name: 'Charles Kayser'})-[:actor]->(movie:movie)<-[:actor]-(p2:person {name: 'John Ott'})
        WHERE NOT (:person {name: 'Drew Barrymor'})-[:actor]->(movie)
        RETURN movie.title
    """)

    print("\nAtores com mais de 30 filmes:\n")

    search("""
        MATCH (person:person)-[:actor]->(movie:movie) 
        WITH person, count(movie) AS qtd_movies
        WHERE qtd_movies > 30
        RETURN person.name, qtd_movies
    """)

    print("\nDiretores de filmes com avaliação maior que 7 do gênero comedia:\n")

    search("""
        MATCH (person:person)-[:director]->(movie:movie) 
        WITH person, movie, count(movie) AS qtd_movies
        WHERE movie.rating > 7 AND 'Comedy' IN movie.genres
        RETURN person.name, qtd_movies
   """)
