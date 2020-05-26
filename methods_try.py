from neo4j import GraphDatabase
import csv


driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

class DBHelpers:
    def __init__(self, uri, auth_tuple):
        # driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))
        self.driver1 = GraphDatabase.driver(uri, auth=auth_tuple)

    def tutors_courses(self,tx, firstname, lastname):
        subjects = tx.run("match (t:Tutor {firstname:$tname, lastname:$tlastname})-[:Teaches]->(s:Subject) return s.name", tname=firstname,tlastname=lastname)
        for subject in subjects:
            print(subject[0])

    def tutors_department(self, tx, firstname, lastname):
        faculty = tx.run("match (t:Tutor {firstname:$fname,lastname:$flastname})-[:WorksIn]->(d:Faculty) return d.name",fname=firstname,flastname=lastname)
        for facult in faculty:
            print("Wydział",facult[0])

    def tutors_who_teaches_many_subjects(self, tx, number):
        count=tx.run("match (t:Tutor)-[r:Teaches]->() with t,count(r) as suma where suma>$num return t", num=number)
        for c in count:
            for attr in c:
                print(attr['degree'],attr['firstname'],attr['lastname'],attr['mail'])

    def required_subjects(self, tx, sub=None):
        required = tx.run("Match (p:Subject{name:$subject})-[*]->(n:Subject) return n.name", subject = sub)
        print("Żeby rozpocząć ten kurs, musisz ukończyć następujące kursy:")
        for s in required:
            print(s[0])

    def get_available_subjects(self, tx, firstname, lastname, pesel=None):
        result = tx.run("MATCH (s:Student {firstname: $firstname, lastname: $lastname})-[:Completed*1..2]->(:Subject)<-[:Require]-(sub:Subject) RETURN  sub", firstname=firstname, lastname=lastname)
        return [item['sub'] for item in result]


    def missing_required_subjects(self, tx, sub=None, album_nr = None):
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
            print("Student może iść na dany kurs")
        else:
            print("Student musi zaliczyć następujące kursy")
            print(difference)


    def faculty_subjects(self, tx, faculty_name):
        subs = tx.run("MATCH (:Faculty {name : $faculty})-[r:BelongsTo]-(b) RETURN b.name", faculty = faculty_name)
        print("Wydział", faculty_name, " prowadzi następujące przedmioty:")
        for i in subs:
            print(i[0])
        

#with driver1.session() as session:
    # session.write_transaction(tutors_courses,"Robert", "Marcjan")
    # session.write_transaction(tutors_department,"Robert", "Marcjan")
    # session.write_transaction(tutors_who_teaches_many_subjects,4)
    # session.write_transaction(required_subjects, "Fizyka 1")
    # session.write_transaction(missing_required_subjects, "Fizyka 1", "220117")
    # session.write_transaction(faculty_subjects, "Elektroniki")

ret = driver1.session().run("MATCH (a:Subject) RETURN a")
