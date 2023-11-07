from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setQuery("""
SELECT DISTINCT ?companyLabel ?employees
WHERE {
  ?company wdt:P31/wdt:P279* wd:Q4830453 . 
  ?company wdt:P159/wdt:P131* wd:Q212 . 
  ?company wdt:P1128 ?employees . 

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY DESC(?employees)
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print("Query results:")
for result in results["results"]["bindings"]:
    company_label = result["companyLabel"]["value"]
    employees = result["employees"]["value"]


    if int(employees) > 1000:
        comment = "This company has a large number of employees."
    else:
        comment = "This company has a small number of employees."


    print(f"Company: {company_label}")
    print(f"Number of employees: {employees}")
    print(comment)
    print("====================================")