from neo4j import GraphDatabase
import csv

driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

def tutors_courses(tx, firstname, lastname):
    subjects = tx.run("match (t:Tutor {firstname:$tname, lastname:$tlastname})-[:Teaches]->(s:Subject) return s.name", tname=firstname,tlastname=lastname)
    for subject in subjects:
        print(subject[0])


def tutors_department(tx, firstname, lastname):
    faculty = tx.run("match (t:Tutor {firstname:$fname,lastname:$flastname})-[:WorksIn]->(d:Faculty) return d.name",fname=firstname,flastname=lastname)
    for facult in faculty:
        print("Wydział",facult[0])

def tutors_who_teaches_many_subjects(tx, number):
    count=tx.run("match (t:Tutor)-[r:Teaches]->() with t,count(r) as suma where suma>$num return t", num=number)
    for c in count:
        for attr in c:
            print(attr['degree'],attr['firstname'],attr['lastname'],attr['mail'])

with driver1.session() as session:
    session.write_transaction(tutors_courses,"Robert", "Marcjan")
    session.write_transaction(tutors_department,"Robert", "Marcjan")
    session.write_transaction(tutors_who_teaches_many_subjects,4)