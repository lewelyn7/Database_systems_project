from neo4j import GraphDatabase
import csv
from pandas import DataFrame


driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

class DBHelpers:
    def __init__(self, uri, auth_tuple):
        # driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))
        self.driver1 = GraphDatabase.driver(uri, auth=auth_tuple)
def tutors_courses(tx, firstname, lastname):
    subjects = tx.run("match (t:Tutor {firstname:$tname, lastname:$tlastname})-[:Teaches]->(s:Subject) return s.name", tname=firstname,tlastname=lastname)
    print(firstname, " ",lastname,"uczy:")
    for subject in subjects:
        print(subject[0])

def tutors_department(tx, firstname, lastname):
    faculty = tx.run("match (t:Tutor {firstname:$fname,lastname:$flastname})-[:WorksIn]->(d:Faculty) return d",fname=firstname,flastname=lastname)
    print(firstname,lastname,"należy do wydziału:")
    faculty = [item[0] for item in faculty]
    print(faculty[0]['name'])


def tutors_who_teaches_many_subjects(tx, number):
    count=tx.run("match (t:Tutor)-[r:Teaches]->() with t,count(r) as suma where suma>$num return t.degree, t.firstname, t.lastname, t.mail", num=number)
    print("\nProwadzący więcej niż", number,"przedmiotów:")
    print(DataFrame(count.data()))
  

def required_subjects(tx, sub=None):
    required = tx.run("Match (p:Subject{name:$subject})-[*]->(n:Subject) return n.name", subject = sub)
    print("\nŻeby rozpocząć ten kurs, musisz ukończyć następujące kursy:")
    for s in required:
        print(s[0])
        
        
def missing_required_subjects(tx, sub=None, album_nr = None):
    required = tx.run("Match (p:Subject{name:$subject})-[*]->(n:Subject) return n.name", subject = sub)
    student_info = tx.run("MATCH (:Student {student_nr : $album})-[r:Completed]-(b)RETURN b.name", album = album_nr)
    subs = []
    info=[]
    for i in student_info:
        info.append(i[0])
    for s in required:
        subs.append(s[0])
    difference = [x for x in subs if x not in info]
    if(len(difference) == 0):
        print("\nStudent może iść na dany kurs")
    else:
        print("\nStudent musi zaliczyć następujące kursy")
        print(difference)


def faculty_subjects(tx, faculty_name):
    subs = tx.run("MATCH (:Faculty {name : $faculty})-[r:BelongsTo]-(b) RETURN b.name as subject_name", faculty = faculty_name)
    print("\nWydział", faculty_name, "prowadzi następujące przedmioty:")
    print(DataFrame(subs.data()))
    # for i in subs:
    #     print(i[0])

def students_in_subject(tx,course_name):
    count = tx.run("match (c:Subject {name: $course})-[:Attends]-(p:Student) return count(p)",course=course_name)
    count = [c[0] for c in count]
    print("\nW kursie",course_name,"uczestniczy", count[0],"studentów.")

def courses_available_for_student(tx, album_nr):
    courses = tx.run("match (s:Student {student_nr: $num})-[:Completed]->(:Subject)<-[:Require]-(sub:Subject) return distinct sub.name", num=album_nr)
    print("\nDostępne przedmioty dla studenta o numerze",album_nr,":")
    lis= [course[0] for course in courses]
    print(DataFrame(lis))

with driver1.session() as session:
    session.write_transaction(tutors_courses,"Robert", "Marcjan")
    session.write_transaction(tutors_department,"Robert", "Marcjan")
    session.write_transaction(tutors_who_teaches_many_subjects,4)
    session.write_transaction(required_subjects, "Fizyka 1")
    session.write_transaction(missing_required_subjects, "Fizyka 1", "220117")
    session.write_transaction(faculty_subjects, "Elektroniki")
    session.write_transaction(students_in_subject, "Cytofizjologia")
    session.write_transaction(courses_available_for_student, "220071")
