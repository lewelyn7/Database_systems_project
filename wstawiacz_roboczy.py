from neo4j import GraphDatabase
import csv

# class HelloWorldExample(object):

#     def __init__(self, uri, user, password):
#         self._driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self._driver.close()

#     def print_greeting(self, message):
#         with self._driver.session() as session:
#             greeting = session.write_transaction(self._create_and_return_greeting, message)
#             print(greeting)

#     @staticmethod
#     def _create_and_return_greeting(tx):
#         result = tx.run("CREATE (a:Greeting) "
#                         "SET a.message = $message "
#                         "RETURN a.message + ', from node ' + id(a)", message=message)
#         return result.single()[0]


driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

def create_subjects(tx):
    infile = open("przedmioty.csv", "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        print(row[0])
        tx.run("CREATE (a:Subject) SET a.name = $name", name=row[0])

def create_tutors(tx):
    infile = open("wykladowcy.csv", "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        print(row[0])
        tx.run("CREATE (a:Tutor) SET a.firstname = $firstname, a.lastname = $lastname, a.mail = $mail, a.degree = $degree", firstname=row[1], lastname=row[0], mail=row[3], degree=row[2])


with driver1.session() as session:
    session.write_transaction(create_tutors)