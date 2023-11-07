from rdflib import Graph
from collections import defaultdict

graph = Graph()
graph.parse('countrues_info.ttl')

country_population = defaultdict(int)

population_query = """
SELECT ?country ?population
WHERE {
    ?country :country_name ?c_name ;
             :population ?population .
}
"""

population_results = graph.query(population_query)
for row in population_results:
    country_uri = row['country']
    population = int(row['population'])
    country_population[country_uri] = population

countries_by_continent = defaultdict(list)

continent_query = """
SELECT ?country ?continent
WHERE {
    ?country :country_name ?c_name ;
             :part_of_continent ?continent .
}
"""

continent_results = graph.query(continent_query)
for row in continent_results:
    country_uri = row['country']
    continent = row['continent']
    countries_by_continent[continent].append((country_uri, country_population[country_uri]))

top_countries_by_continent = {}
for continent, countries in countries_by_continent.items():
    countries.sort(key=lambda x: x[1], reverse=True)
    top_countries_by_continent[continent] = countries[:5]

for continent, top_countries in top_countries_by_continent.items():
    print(f"Continent: {continent}")
    for country_uri, population in top_countries:
        country_name_query = f"""
        SELECT ?c_name
        WHERE {{
            <{country_uri}> :country_name ?c_name .
        }}
        """
        country_name_results = graph.query(country_name_query)
        for country_name_result in country_name_results:
            country_name = country_name_result['c_name']
            print(f"Country: {country_name}, Population: {population}")
    print()
