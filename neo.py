from neo4j import GraphDatabase
from py2neo import Graph

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost"
AUTH = ("-", "-")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

# records, summary, keys = driver.execute_query(
#     "	MATCH (n) RETURN n LIMIT 25",
#     database_="staff",
# )
#
# # Loop through results and do something with them
# for person in records:
#     print(person.data())
#
# # Summary information
# print("The query `{query}` returned {records_count} records in {time} ms.".format(
#     query=summary.query, records_count=len(records),
#     time=summary.result_available_after,
# ))

def find_direc():
    records, summary, keys = driver.execute_query("Match (n:Director) return n", database_="staff")
    return records

def find_admin():
    records, summary, keys = driver.execute_query("Match (n:Administrator) return n", database_="staff")
    return records

def find_washer():
    records, summary, keys = driver.execute_query("Match (n:Washer) return n", database_="staff")
    return records
