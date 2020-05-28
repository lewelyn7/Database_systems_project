from neo4j import GraphDatabase
import csv
from pandas import DataFrame



class DBHelpers:
    def __init__(self, uri, auth_tuple):
        # driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))
        self.driver1 = GraphDatabase.driver(uri, auth=auth_tuple)

    @staticmethod
    def tutors_courses(tx, firstname, lastname): # subjects which are tought by tutor
        result = tx.run("match (t:Tutor {firstname:$tname, lastname:$tlastname})-[:Teaches]->(s:Subject) return s", tname=firstname,tlastname=lastname)
        return [item['s'] for item in result]


    @staticmethod
    def tutors_department(tx, firstname, lastname): # returns tutor's department
        faculty = tx.run("match (t:Tutor {firstname:$fname,lastname:$flastname})-[:WorksIn]->(d:Faculty) return d",fname=firstname,flastname=lastname)
        return [item[0] for item in faculty]

    @staticmethod
    def tutors_who_teaches_many_subjects(tx, number): # returns all tutors who teaches more than $number subjects
        count=tx.run("match (t:Tutor)-[r:Teaches]->() with t,count(r) as suma where suma>$num return t", num=number)
        return [item['t'] for item in count]
  
    @staticmethod 
    def required_subjects(tx, sub): # returns all required subject needed to start specified subject
        required = tx.run("match (n:Subject {name:$sub}), (s:Subject {tier: 1}) with n,collect(s) as col unwind col as c with collect( case  when n in col then [] else nodes(shortestPath((c)-[:Require*]-(n))) end) as result,n unwind result as res return min(res) as n", sub = sub)
        a= [item['n'] for item in required]
        return a[0]
    
    @staticmethod # returns whether or not student can attend to that course
    def missing_required_subjects(tx, sub, album_nr):
        required = tx.run("match (n:Subject {name:$sub}), (s:Subject {tier: 1}) with n,collect(s) as col unwind col as c with collect( case  when n in col then [] else nodes(shortestPath((c)-[:Require*]-(n))) end) as result,n unwind result as res return min(res) as n", sub = sub)
        student_info = tx.run("MATCH (:Student {student_nr : $album})-[r:Completed | Attends]-(b)RETURN b.name", album = album_nr)
        subs = []
        info=[]
        for i in student_info:
            info.append(i[0])
        for s in required:
            subs.append(s[0])

        difference = [x for x in subs if x not in info]
        if(len(difference[0]) == 0):
            return 'ok'
        else:
            return difference[0]

#does the same as missing_required_subjects but in other way
    @staticmethod
    def shortest_subject_path(tx,album_nr, subject_name): 
        path = tx.run("match (n:Subject {name:$sub}), (s:Subject {tier: 1}) with n,collect(s) as col unwind col as c with collect( case  when n in col then [] else nodes(shortestPath((c)-[:Require*]-(n))) end) as result,n unwind result as res return min(res)", sub = subject_name)
        path2 = tx.run("match (find:Subject {name:$name}), (student:Student {student_nr:$nr})-[completed:Completed | Attends]-(sub), p1=shortestPath((sub)-[:Require*]-(find)) return  nodes(p1) order by size(nodes(p1)) LIMIT 1", nr=album_nr, name=subject_name)
        lis1 = [x[0] for x in path ]
        lis2 = [x[0] for x in path2] 
        
        if(len(lis1)<len(lis2)):
            sh_path=lis1
        else:
            sh_path=lis2

        if(len(lis2)==0):
            sh_path=lis1
        return sh_path[0]
    @staticmethod
    def faculty_subjects(tx, faculty_name): # Subjects which belong to a specified department
        subs = tx.run("MATCH (:Faculty {name : $faculty})-[r:BelongsTo]-(b) RETURN b", faculty = faculty_name)
        return [item['b'] for item in subs]

    @staticmethod
    def students_in_subject(tx,course_name): # return how many studenst attends to a course and their properties
        count = tx.run("match (c:Subject {name: $course})-[:Attends]-(p:Student) return count(p)",course=course_name)
        return [c[0] for c in count]


    @staticmethod
    def courses_available_for_student(tx, album_nr): # returns courses available for student based on his completed courses 
        courses = tx.run("match (s:Student {student_nr:$num})-[:Completed]->(comp:Subject),(s)-[:Attends]->(att:Subject) with collect(comp) as subs, s, collect(att) as attry unwind subs as sub match (sub)<-[:Require]-(f:Subject) where f.free_places>0 and not f in subs and not f in attry return distinct f", num=album_nr)
        coursertier1=tx.run("match (s:Subject {tier:1}) where s.free_places>0 return s")
        return [course['f'] for course in courses]+[cours['s'] for cours in coursertier1]

    @staticmethod
    def get_student_info(tx, firstname=None, lastname=None, pesel=None, student_nr=None): # returns information about all student with specified firstname, surname, pesel, student_nr 
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
    def get_tutor_info(tx, firstname=None, lastname=None, degree=None, mail=None): # returns information about all tutors with specified firstname, surname, pesel, student_nr 
        query = "MATCH (s:Tutor) WHERE "
        if firstname:
            query += "s.firstname = $firstname and "
        if lastname:
            query += "s.lastname = $lastname and "
        if degree:
            query += "s.degree = $degree and "
        if mail:
            query += "s.mail = $mail and"
        query += " 1=1 RETURN s"

        result = tx.run(query, firstname=firstname, lastname=lastname, degree=degree, mail=mail).data()
        return [item['s'] for item in result]


    @staticmethod
    def get_student_completed_courses(tx, firstname=None, lastname=None, pesel=None, student_nr=None): # returns information about all student with specified firstname, surname, pesel, student_nr 
        query = "MATCH (s:Student)-[:Completed]->(sub:Subject) WHERE "
        if firstname:
            query += "s.firstname = $firstname and "
        if lastname:
            query += "s.lastname = $lastname and "
        if pesel:
            query += "s.pesel = $pesel and "
        if student_nr:
            query += "s.student_nr = $student_nr and"
        query += " 1=1  return sub"

        result = tx.run(query, firstname=firstname, lastname=lastname, pesel=pesel, student_nr=student_nr).data()
        return [item['sub'] for item in result]


    @staticmethod
    def get_student_attends_courses(tx, firstname=None, lastname=None, pesel=None, student_nr=None): # returns information about all student with specified firstname, surname, pesel, student_nr 
        query = "MATCH (s:Student)-[:Attends]->(sub:Subject) WHERE "
        if firstname:
            query += "s.firstname = $firstname and "
        if lastname:
            query += "s.lastname = $lastname and "
        if pesel:
            query += "s.pesel = $pesel and "
        if student_nr:
            query += "s.student_nr = $student_nr and"
        query += " 1=1  return sub"

        result = tx.run(query, firstname=firstname, lastname=lastname, pesel=pesel, student_nr=student_nr).data()
        return [item['sub'] for item in result]



    @staticmethod
    def subjects_belong_to_few_departments(tx): # returns subjects which belong to more than one faculty
        subs=tx.run("match (s:Subject)-[b:BelongsTo]->(:Faculty) with s,count(b) as cou where cou>1 return s")
        return [sub['s'] for sub in subs]
    
    @staticmethod
    def add_student(tx, firstname, lastname, pesel, album_nr):
        if(len(firstname)==0 or len(lastname)==0 or len(pesel)<11 or len(album_nr)<6):
            return -1
        person=tx.run("match (s: Student) where s.pesel=$pesel or s.student_nr=$album_nr return s", pesel=pesel, album_nr=album_nr)
        if(person.data()==[]):
            tx.run("create (n:Student {firstname:$firstname, lastname:$lastname, pesel:$pesel, student_nr:$album_nr})",firstname=firstname,lastname=lastname, pesel=pesel, album_nr=album_nr)
            return 0
        else:
            return 1
    
    @staticmethod
    def add_tutor(tx, degree, firstname, lastname, mail, faculty):
        if(len(firstname)==0 or len(lastname)==0  or  '@' not in mail or len(mail)<5 or len(faculty)==0):
            return -1
        person=tx.run("match (s: Tutor) where s.mail=$mail return s", mail=mail)
        if(person.data()==[]):
            fa = tx.run("match (f:Faculty {name:$name}) return f", name=faculty)
            if(fa.data()==[]):
                return 1
            
            tx.run("match (f:Faculty {name:$name}) create (n:Tutor {firstname:$firstname, lastname:$lastname, degree:$degree, mail:$mail})-[:WorksIn]->(f)", name=faculty,firstname=firstname,lastname=lastname, degree=degree, mail=mail)
            return 0
        else:
            return 1
    
    @staticmethod
    def add_subject(tx, name, max_students,faculty, tier, requires=None): 
        if(len(name)==0 or len(faculty)==0  or tier<1 or tier>7 or max_students<0):
            return -1
        sub=tx.run("match (s: Subject) where s.name=$name return s", name=name)

        if(sub.data()==[]):
            fa = tx.run("match (f:Faculty {name:$name}) return f", name=faculty)
            if(fa.data()==[]):
                return -1

            tx.run("match (f:Faculty {name:$fac}) create (n:Subject {name:$name, maxstudents:$maxst, tier:$tier})-[:BelongsTo]->(f)",name=name,maxst=max_students, tier=tier,fac=faculty)
            
            if requires:
                req = tx.run("match (f:Subject {name:$requ}) return f", requ=requires)
                if(req.data()==[]):
                    return 1
                else:
                    tx.run("match (s:Subject {name: $name}), (req:Subject {name:$reqname}) create (s)-[:Require]->(req)", name=name, reqname=requires)
            return 0
        else:
            return 1
        
        
    @staticmethod   
    def sign_up(tx, course_name, student_nr):
        if tx.run("MATCH (s:Student {student_nr : $number})-[r]->(n:Subject {name : $name}) RETURN count(r)", number = student_nr, name = course_name).single()[0] != 0:
            print("Student has already been signed up or completed this course")
            return False
        if(DBHelpers.missing_required_subjects(tx, course_name, student_nr) == 'ok'):
            students=tx.run("MATCH (n:Subject {name : $name}) return n.free_places",name = course_name)
            ns=[item['n.free_places'] for item in students]
            if(ns[0]>0):
                tx.run("MATCH (n:Subject {name : $name}) SET n.free_places=n.free_places-1",name = course_name)
                tx.run("MATCH (s:Student {student_nr : $number}),(n:Subject {name : $name}) CREATE (s)-[r:Attends]->(n)", number = student_nr, name = course_name)
                return True
            else:
                print("Student cannot be signed up - no free places")
                return False
        else:
            print("Student cannot be signed up - requirements not met")
            return False
    

    @staticmethod   
    def complete_course(tx, course_name, student_nr):
        if(tx.run("MATCH (s:Student {student_nr : $number})-[r:Attends]->(n:Subject {name : $name}) RETURN count(r)", number = student_nr, name = course_name).single()[0] == 0 ):
            print("Wrong given arguments - cannot complete course")
            return False
        else:
            tx.run("MATCH (s:Student {student_nr : $number}),(n:Subject {name : $name}) CREATE (s)-[r:Completed]->(n)", number = student_nr, name = course_name)
            tx.run("MATCH (s:Student {student_nr : $number})-[r:Attends]->(n:Subject {name : $name}) DELETE r ", number = student_nr, name = course_name)
            tx.run("MATCH (n:Subject {name : $name}) SET n.free_places=n.free_places+1",name = course_name)
            return True


if __name__ == "__main__":
    db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))
    with db.driver1.session() as session:
        pass
        # print(session.write_transaction(DBHelpers.tutors_courses,"Piotr", "Nowak"))
        # print(session.write_transaction(DBHelpers.tutors_department,"Piotr", "Nowak"))
        # print(session.write_transaction(DBHelpers.tutors_who_teaches_many_subjects,4))
        print(session.write_transaction(DBHelpers.required_subjects, "Fizyka 1"))
        # print(session.write_transaction(DBHelpers.missing_required_subjects, "Cytofizjologia", "220195"))

        # print(session.write_transaction(DBHelpers.missing_required_subjects, "Metody i algorytmy sztucznej inteligencji", "220195"))
        # print(session.write_transaction(DBHelpers.faculty_subjects, "Elektroniki"))
        # print(session.write_transaction(DBHelpers.students_in_subject, "Cytofizjologia"))
        # print(session.write_transaction(DBHelpers.courses_available_for_student, "220083"))
        # print(session.write_transaction(DBHelpers.get_student_info, "Alicja"))
        # print(session.write_transaction(DBHelpers.shortest_subject_path, "220195", "Fizyka 1"))
        # print(session.write_transaction(DBHelpers.subjects_belong_to_few_departments))
        # print(session.write_transaction(DBHelpers.add_student, "Krystyna", "Błaszczyk", "82275931473", "320109"))
        # print(session.write_transaction(DBHelpers.add_tutor, "prof.", "Natalia", "Brzozowska", "nbrzozowska@agh.edu.pl", "Informatyki"))
        # print(session.write_transaction(DBHelpers.add_subject,"Metody i algorytmy sztucznej inteligencji",25,"Informatyki",1 ))
        # print(session.write_transaction(DBHelpers.get_tutor_info, "Piotr"))

        # print(session.write_transaction(DBHelpers.get_student_completed_courses, "Alicja"))
        # print(session.write_transaction(DBHelpers.get_student_attends_courses, "Alicja"))
        # print(session.write_transaction(DBHelpers.sign_up,"Metody i algorytmy sztucznej inteligencji", "220083"))
        # print(session.write_transaction(DBHelpers.complete_course,"Metody i algorytmy sztucznej inteligencji", "220083"))
