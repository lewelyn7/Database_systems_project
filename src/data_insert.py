from neo4j import GraphDatabase
from random import randint
import csv

driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

def create_subjects(tx, filename, faculty_name):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    basics_1 = [90, 333, 61, 30, 22, 21, 290]
    basics_2 = [310, 74, 38, 32, 26, 21, 301, 303, 76, 310, 324]
    basics_3 = [322, 336, 91, 65, 33, 345, 316, 280, 273]
    basics_4 = [331, 335, 77, 81, 24, 342, 306, 297, 278, 81, 39]
    basics_5 = [332, 337, 31, 102, 104, 28, 277, 305, 326]
    basics_6 = [315, 325, 70, 109, 199, 300, 275, 327, 282, 199]
    for row in csvimport:
        print(row[0])
        result = tx.run("MATCH (n:Subject { name : $name }) RETURN n", name=row[0])
        if not result.single():
            rand_tier = randint(1, 7)
            tx.run("CREATE (a:Subject) SET a.name = $name, a.tier = $tier", name=row[0], tier = rand_tier)
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)
        else:
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)
        
        
        i = randint(0, 6) #zmieniany zakres w zależności od poziomu
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 2 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_1[i])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 3 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_2[i])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 4 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_3[i])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 5 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_4[i])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 6 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_5[i])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 7 and id(b) = $id Create (a)-[r: Require]->(b)", name = row[0], id = basics_6[i])

def create_tutors(tx, lecturers_file, faculty_name):
    infile = open(lecturers_file, "r")  
    csvimport = csv.reader(infile)
    subjectnum = tx.run("MATCH (a:Subject)-[r:BelongsTo]->(b:Faculty { name : $faculty }) WITH count(a) AS value RETURN value", faculty=faculty_name).single()[0]
    subjects = list(tx.run("MATCH (a:Subject)-[r:BelongsTo]->(b:Faculty {name : $faculty}) RETURN a", faculty=faculty_name).__iter__())
    print(subjectnum)
    for row in csvimport:
        print(row[0])
        tx.run("CREATE (a:Tutor) SET a.firstname = $firstname, a.lastname = $lastname, a.mail = $mail, a.degree = $degree", firstname=row[1], lastname=row[0], mail=row[3], degree=row[2])
        tx.run("MATCH (a:Tutor { firstname: $firstname, lastname: $lastname}), (b:Faculty { name : $faculty }) CREATE (a)-[r:WorksIn]->(b)", firstname=row[1], lastname=row[0], faculty=faculty_name)
        
        numberofsubjects = randint(1,5)
        for i in range(numberofsubjects):
            randomnum = randint(0, subjectnum-1)
            tx.run("MATCH (a:Tutor { firstname: $firstname, lastname: $lastname}), (s:Subject { name : $subject }) CREATE (a)-[r:Teaches]->(s)", firstname=row[1], lastname=row[0], subject=subjects[randomnum]["a"]["name"])

def create_students(tx, filename):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        if (p % 3 == 0):
            tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 90 and b.tier = 1 CREATE (a)-[r:Attends]->(b)",
                pesel=row[2])
        else:
            if (p % 3 == 1):
                tx.run("MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 90 and b.tier = 1 CREATE (a)-[r:Completed]->(b)",
                pesel=row[2])
        if (p % 2 == 0):
            tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 333 and b.tier = 1 CREATE (a)-[r:Completed]->(b)",
                pesel=row[2])
        else:
            tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 333 and b.tier = 1 CREATE (a)-[r: Attends]->(b)",
                pesel=row[2])
        if (p % 5 == 0):
            tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 61 and b.tier = 1 CREATE (a)-[r:Attends]->(b)",
                pesel=row[2])
        else:
            if (p % 5 == 3):
                tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 61 and b.tier = 1 CREATE (a)-[r:Completed]->(b)",
                pesel=row[2])
        if( p % 10 == 0):
            tx.run(
                "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 30 and b.tier = 1 CREATE (a)-[r:Completed]->(b)",
                pesel=row[2])
        else:
            if(p % 10 == 7):
                tx.run(
                    "MATCH (a:Student), (b:Subject) WHERE a.pesel = $pesel and id(b) = 30 and b.tier = 1 CREATE (a)-[r:Attends]->(b)",
                    pesel=row[2])
        p += 1
        
if __name__ == '__main__':

    with driver1.session() as session:
        session.write_transaction(create_subjects, "przedmioty.csv", "Informatyki")
        session.write_transaction(create_subjects, "przedmioty2.csv", "Elektroniki")
        session.write_transaction(create_subjects, "przedmioty3.csv", "Fizyki Medycznej")
        session.write_transaction(create_students, "students.csv")
