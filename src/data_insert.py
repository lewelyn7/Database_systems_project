from neo4j import GraphDatabase
from random import randint
import csv

driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

def create_subjects(tx, filename, faculty_name):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)

    for row in csvimport:
        print(row[0])
        result = tx.run("MATCH (n:Subject { name : $name }) RETURN n", name=row[0])
        if not result.single():
            rand_tier = randint(1, 7)
            tx.run("CREATE (a:Subject) SET a.name = $name, a.tier = $tier", name=row[0], tier = rand_tier)
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)
        else:
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)
        
    basics_1 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=1).data()
    basics_2 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=2).data()
    basics_3 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=3).data()
    basics_4 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=4).data()
    basics_5 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=5).data()
    basics_6 = tx.run("MATCH (s:Subject { tier : $tier}) RETURN id(s) as id", tier=6).data()
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        i = randint(0, 6) #zmieniany zakres w zależności od poziomu
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 2 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_1[randint(0, len(basics_1)-1)]['id'])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 3 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_2[randint(0, len(basics_2)-1)]['id'])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 4 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_3[randint(0, len(basics_3)-1)]['id'])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 5 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_4[randint(0, len(basics_4)-1)]['id'])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 6 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_5[randint(0, len(basics_5)-1)]['id'])
        tx.run("Match (a:Subject), (b:Subject) where a.name = $name and a.tier = 7 and id(b) = $id Create (a)-[r:Require]->(b)", name = row[0], id = basics_6[randint(0, len(basics_6)-1)]['id'])


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
def add_students(tx, filename):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        tx.run("CREATE (s:Student) SET s.firstname = $firstname, s.lastname = $lastname, s.pesel = $pesel, s.student_nr= $student_nr ", firstname=row[0], lastname=row[1], pesel=row[2], student_nr=row[3])

def sign_students(tx, filename):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    tiers = []
    for i in range(1,8):
        tiers.append(tx.run("MATCH (s:Subject { tier : $tier}) RETURN s.name as id", tier=i).data())
    print(tiers)
    # print(tiers)
    for row in csvimport:
        print(row[2], end=' ')
        randnum = randint(1,100)
        print(randnum)
        if(randnum < 6):
            continue
        randnum2 = randint(0, len(tiers[0])-1)
        tx.run("MATCH (s:Student {pesel: $pesel}), (b:Subject) WHERE b.name=$subid CREATE (s)-[r:Completed]->(b)", pesel=row[2], subid=tiers[0][randnum2]['id'])
        thresholds = [6, 30, 40, 50, 60, 70,80, 90]
        for i in range(1,8):
            courses_ava = tx.run("match (s:Student {pesel: $pesel})-[:Completed]->(:Subject)<-[:Require]-(sub:Subject) return distinct sub.name as id", pesel=row[2]).data()
            courses1 = [item['id'] for item in courses_ava]
            completed_courses_dict = tx.run("match (s:Student {pesel: $pesel})-[:Completed]->(sub:Subject) return sub.name as id", pesel=row[2]).data()
            completed_courses = [item['id'] for item in completed_courses_dict]
            courses = list(set(courses1) - set(completed_courses))
            print(courses)
            if courses: 
                if(randnum > thresholds[i]):
                    randomcourse = randint(0,len(courses)-1)
                    print(courses[randomcourse])
                    tx.run("MATCH (s:Student {pesel: $pesel}), (b:Subject) WHERE b.name=$subid CREATE (s)-[r:Completed]->(b)", pesel=row[2], subid=courses[randomcourse])

#not documented
def set_attends_rel(tx, filename):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)

    for row in csvimport:
            courses_ava = tx.run("match (s:Student {pesel: $pesel})-[:Completed]->(:Subject)<-[:Require]-(sub:Subject) return distinct sub.name as id", pesel=row[2]).data()
            courses1 = [item['id'] for item in courses_ava]
            completed_courses_dict = tx.run("match (s:Student {pesel: $pesel})-[:Completed]->(sub:Subject) return sub.name as id", pesel=row[2]).data()
            completed_courses = [item['id'] for item in completed_courses_dict]
            courses = list(set(courses1) - set(completed_courses))
            how_many = randint(0, len(courses))
            print(row[2] + " " + str(how_many))
            print(courses)
            for i in range(how_many):
                tx.run("MATCH (s:Student {pesel: $pesel}), (sb:Subject {name: $name}) CREATE (s)-[:Attends]->(sb)", pesel=row[2], name=courses[i])

        
if __name__ == '__main__':

    with driver1.session() as session:
        # session.write_transaction(create_subjects, "przedmioty.csv", "Informatyki")
        # session.write_transaction(create_subjects, "przedmioty2.csv", "Elektroniki")
        # session.write_transaction(create_subjects, "przedmioty3.csv", "Fizyki Medycznej")
        # session.write_transaction(create_tutors, "wykladowcy.csv", "Informatyki")
        # session.write_transaction(create_tutors, "wykladowcy2.csv", "Elektroniki")
        # session.write_transaction(create_tutors, "wykladowcy3.csv", "Fizyki Medycznej")
        # session.write_transaction(add_students, "students.csv")
        # session.write_transaction(sign_students, "students.csv")
        set_attends_rel(session, "data/students.csv")
