from neo4j import GraphDatabase
import csv
from pandas import DataFrame


driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

class DBHelpers:
    def __init__(self, uri, auth_tuple):
        # driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))
        self.driver1 = GraphDatabase.driver(uri, auth=auth_tuple)

    @staticmethod
    def tutors_courses(tx, firstname, lastname):
        subjects = tx.run("match (t:Tutor {firstname:$tname, lastname:$tlastname})-[:Teaches]->(s:Subject) return s.name", tname=firstname,tlastname=lastname)
        print(firstname, " ",lastname,"uczy:")
        for subject in subjects:
            print(subject[0])

    @staticmethod
    def tutors_department(tx, firstname, lastname):
        faculty = tx.run("match (t:Tutor {firstname:$fname,lastname:$flastname})-[:WorksIn]->(d:Faculty) return d",fname=firstname,flastname=lastname)
        print(firstname,lastname,"należy do wydziału:")
        faculty = [item[0] for item in faculty]
        print(faculty[0]['name'])

    @staticmethod
    def tutors_who_teaches_many_subjects(tx, number):
        count=tx.run("match (t:Tutor)-[r:Teaches]->() with t,count(r) as suma where suma>$num return t.degree, t.firstname, t.lastname, t.mail", num=number)
        print("\nProwadzący więcej niż", number,"przedmiotów:")
        print(DataFrame(count.data()))
  
    @staticmethod
    def required_subjects(tx, sub=None):
        required = tx.run("Match (p:Subject{name:$subject})-[*]->(n:Subject) return n.name", subject = sub)
        print("\nŻeby rozpocząć ten kurs, musisz ukończyć następujące kursy:")
        for s in required:
            print(s[0])
        
    @staticmethod
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

    @staticmethod
    def faculty_subjects(tx, faculty_name):
        subs = tx.run("MATCH (:Faculty {name : $faculty})-[r:BelongsTo]-(b) RETURN b.name as subject_name", faculty = faculty_name)
        print("\nWydział", faculty_name, "prowadzi następujące przedmioty:")
        print(DataFrame(subs.data()))
        # for i in subs:
        #     print(i[0])

    @staticmethod
    def students_in_subject(tx,course_name):
        count = tx.run("match (c:Subject {name: $course})-[:Attends]-(p:Student) return count(p)",course=course_name)
        count = [c[0] for c in count]
        print("\nW kursie",course_name,"uczestniczy", count[0],"studentów.")

    @staticmethod
    def courses_available_for_student(tx, album_nr):
        courses = tx.run("match (s:Student {student_nr: $num})-[:Completed]->(:Subject)<-[:Require]-(sub:Subject) return distinct sub.name", num=album_nr)
        print("\nDostępne przedmioty dla studenta o numerze",album_nr,":")
        lis= [course[0] for course in courses]
        print(DataFrame(lis))
        return lis

    @staticmethod
    def get_student_info(tx, firstname=None, lastname=None, pesel=None, student_nr=None):
        query = "MATCH (s:Student) WHERE "
        if firstname:
            query += "s.firstname = $firstname and "
        if lastname:
            query += "s.lastname = $lastname and "
        if pesel:
            query += "s.pesel = $pesel and "
        if student_nr:
            query += "s.student_nr = $student_nr and"
        query += " 1=1 RETURN s"

        result = tx.run(query, firstname=firstname, lastname=lastname, pesel=pesel, student_nr=student_nr).data()
        return [item['s'] for item in result]
    
    @staticmethod
    def shortest_subject_path(tx,album_nr, subject_name):
        path = tx.run("match (s:Student {student_nr:$num}), (n:Subject {name:$name}), p=shortestPath((s)-[:Completed | Require *]-(n)) return nodes(p)",num=album_nr, name=subject_name)
        lis = [x[0] for x in path ]
        print(DataFrame(lis))
        # for y in lis:
        #     if(y[labels]=='Student'):
        #         print(y['firstname'])
        
        return #path trzeba tu jakoś dobrze zwracać coś ale nwm do kończa co ide spać 

session = driver1.session()



with driver1.session() as session:
    # session.write_transaction(DBHelpers.tutors_courses,"Robert", "Marcjan")
    # session.write_transaction(DBHelpers.tutors_department,"Robert", "Marcjan")
    # session.write_transaction(DBHelpers.tutors_who_teaches_many_subjects,4)
    # session.write_transaction(DBHelpers.required_subjects, "Fizyka 1")
    # session.write_transaction(DBHelpers.missing_required_subjects, "Fizyka 1", "220117")
    # session.write_transaction(DBHelpers.faculty_subjects, "Elektroniki")
    # session.write_transaction(DBHelpers.students_in_subject, "Cytofizjologia")
    # session.write_transaction(DBHelpers.courses_available_for_student, "220071")
    print(session.write_transaction(DBHelpers.get_student_info, "Alicja"))
    session.write_transaction(DBHelpers.shortest_subject_path, "220071", "Wychowanie fizyczne 1")
