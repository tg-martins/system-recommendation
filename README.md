
# Sistemas de recomendação de filmes

EP 02 de ciência de dados, com objetivo de montar grafos ligando os dados e montar um sistema de recomendação utilizando dados do IMDb.


## Atributos do nó pessoa

| Id            |   Name                                                               |
| ----------------- | ---------------------------------------------------------------- |
| nm0022608       | Fernande Albany |
| nm0022607       | Carl Alstrup |
| nm0016317       | Oda Alstrup |

## Atributos do nó filme

| Id              |   Title                 | Genres                      | Rating     |
| ----------------| ------------------------|-----------------------------|---------- |
| tt0000001       | Carmencita              |[Documentary, Short]         |5.7|
| tt0000002       | Le clown et ses chiens  |[Animation, Short]           |5.8|
| tt0000003       | Pauvre Pierrot          |[Animation, Comedy, Romance] |6.5|

## Exemplo das ligações

![Grafos](https://github.com/tg-martins/system-recommendation/blob/main/graphs.png)


## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/tg-martins/system-recommendation
```

Entre no diretório do projeto e inclua os seguintes arquivos do site https://www.imdb.com/interfaces/ na pasta "datasets"

- title.basics.tsv
- title.principals.tsv
- title.ratings.tsv
- name.basics.tsv

Instale as dependências

```bash
  pip install pandas
  pip install neo4j 
```

Execute o script para gerar os grafos

```bash
  python insert.py
```

Execute o script para realizar consultas de teste  
```bash
  python query.py
```

Execute o script para realizar as recomendações com base no filme escolhido 
```bash
  python recommendation.py
```


## Referências

 - [Ne04j](https://neo4j.com/)
 - [IMDb](https://www.imdb.com/interfaces/)

