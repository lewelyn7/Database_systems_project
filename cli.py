from cli_app import App, Command
from pandas import DataFrame
from src.db_helpers import DBHelpers

class GetStudentInfo(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname of student", default=None, required=False)
        parser.add_argument("--lastname", "-l", type=str, help="lastname of student", default=None, required=False)
        parser.add_argument("--pesel", "-p", type=str, help="pesel of student", default=None, required=False)
        parser.add_argument("--album", "-a", type=str, help="album number of student", default=None, required=False)

    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        pesel = self.app.args.pesel
        album = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.get_student_info, fname, lname, pesel, album)
            print(DataFrame(result))


class GetTutorInfo(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname of student", default=None, required=False)
        parser.add_argument("--lastname", "-l", type=str, help="lastname of student", default=None, required=False)
        parser.add_argument("--degree", "-d", type=str, help="degree of tutor", default=None, required=False)
        parser.add_argument("--mail", "-m", type=str, help="tutor's mail to connect with him", default=None, required=False)

    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        degree = self.app.args.degree
        mail = self.app.args.mail
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.get_tutor_info, fname, lname, degree, mail)
            print(DataFrame(result))


class TutorsCourses(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--fname", "-f", type=str, help="firstname of tutor", required=True)
        parser.add_argument("--lname", "-l", type=str, help="lastname of tutor", required=True)

    def run(self):
        fname = self.app.args.fname
        lname = self.app.args.lname
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.tutors_courses, fname, lname)
            print()
            print(fname + " " + lname + "\'s" + " courses:")
            print()
            print(DataFrame(result))        

            
class TutorsDepartment(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--fname", "-f", type=str, help="firstname of tutor", required=True)
        parser.add_argument("--lname", "-l", type=str, help="lastname of tutor", required=True)

    def run(self):
        fname = self.app.args.fname
        lname = self.app.args.lname
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.tutors_department, fname, lname)
            print()
            print(fname + " " + lname + "\'s" + " faculty:")
            print()
            print(DataFrame(result))

            
class TutorsWhoTeachesManySubject(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--number", "-n", type=int, help="number of subjects to compare", required=True)

    def run(self):
        number = self.app.args.number
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.tutors_who_teaches_many_subjects, number)
            print()
            print("Tutors who teaches more than", number,"subjects:")
            print()
            print(DataFrame(result))
            
            
class FewDapartmentsSubjects(Command):
    @staticmethod
    def register_arguments(parser):
        pass

    def run(self):
        faculty_name = self.app.args.fname
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.subjects_belong_to_few_departments, faculty_name)
            print()
            print("Courses:")
            print()
            print(DataFrame(result))
            
            

class RequiredSubjects(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--subject", "-s", type=str, help="returns all required subjects", required=True)

    
    def run(self):
        sub = self.app.args.subject
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.required_subjects, sub)
            print("Required subjects: ")
            print(DataFrame(result))

            
class MissingRequiredSubjects(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--subject", "-s", type=str, help="returns all required subjects", required=True)
        parser.add_argument("--album", "-a", type=str, help="album number of student", required=True)

    
    def run(self):
        sub = self.app.args.subject
        album = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.missing_required_subjects, sub, album)
            print("Missing Required subjects: ")
            if result == "ok":
                print("All required subjects are completed")
            else:
                print(DataFrame(result))       

class FacultySubjects(Command):

    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--faculty", "-f", type=str, help="returns faculty's subjects", required=True)

    
    def run(self):
        fac = self.app.args.faculty
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.faculty_subjects, fac)
            print(fac + "'s subjects: ")
            print(DataFrame(result))

            
class StudentsInSubject(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--subject", "-s", type=str, help="returns students in subject", required=True)

    
    def run(self):
        sub = self.app.args.subject
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.students_in_subject, sub)
            print("Number of students in " + sub)
            print(DataFrame(result))

            
            
class CoursesAvailableForStudents(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--album", "-a", type=str, help="album number of student", required=True)

    
    def run(self):
        alb = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.courses_available_for_student, alb)
            print("Available courses:")
            print(DataFrame(result))


class ShortestSubjectPath(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--album", "-a", type=str, help="album number of student", required=True)
        parser.add_argument("--subject", "-s", type=str, help="subject to be completed", required=True)
  
    def run(self):
        alb = self.app.args.album
        sub = self.app.args.subject
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.shortest_subject_path, alb, sub)
            print("Courses:")
            print(DataFrame(result))

            
class AddStudent(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname", required=True)
        parser.add_argument("--lastname", "-l", type=str, help="lastname", required=True)
        parser.add_argument("--pesel", "-p", type=str, help="pesel", required=True)
        parser.add_argument("--album", "-a", type=str, help="album", required=True)

    
    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        pesel = self.app.args.pesel
        alb = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.add_student, fname, lname, pesel, alb)
            if result == 0:
                print("Student has been added")
            else:
                print("Adding error")

class AddTutor(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname", required=True)
        parser.add_argument("--lastname", "-l", type=str, help="lastname", required=True)
        parser.add_argument("--mail", "-m", type=str, help="mail", required=True)
        parser.add_argument("--faculty", "-c", type=str, help="faculty", required=True)

    
    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        mail = self.app.args.mail
        fac = self.app.args.faculty
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.add_tutor, fname, lname, mail, fac)
            if result == 0:
                print("Tutor has been added")
            else:
                print("Adding error")


class AddSubject(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--name", "-n", type=str, help="firstname", required=True)
        parser.add_argument("--max-student", "-m", type=str, help="lastname", required=True)
        parser.add_argument("--faculty", "-f", type=str, help="mail", required=True)
        parser.add_argument("--tier", "-t", type=int, help="tier", required=True)

    
    def run(self):
        name = self.app.args.name
        maxstud = self.app.args.m
        fac = self.app.args.faculty
        tier = self.app.args.tier
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.add_subject, name, maxstud, fac, tier)
            if result == 0:
                print("Subject has been added")
            else:
                print("Adding error")
                
                
                
class SignUp(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--student_nr", "-s", type=str, help="student number", required=True)
        parser.add_argument("--course_n", "-c", type=str, help="name of corse", required=True)

    def run(self):
        student = self.app.args.student_nr
        course = self.app.args.course_n
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.sign_up, course, student)
            if result:
                print("Signing up successful")


class GetStudentsAttends(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname of student", default=None, required=False)
        parser.add_argument("--lastname", "-l", type=str, help="lastname of student", default=None, required=False)
        parser.add_argument("--pesel", "-p", type=str, help="pesel of student", default=None, required=False)
        parser.add_argument("--album", "-a", type=str, help="album number of student", default=None, required=False)

    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        pesel = self.app.args.pesel
        album = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.get_student_attends_courses, fname, lname, pesel, album)
            print(DataFrame(result))


class GetStudentsCompleted(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--firstname", "-f", type=str, help="firstname of student", default=None, required=False)
        parser.add_argument("--lastname", "-l", type=str, help="lastname of student", default=None, required=False)
        parser.add_argument("--pesel", "-p", type=str, help="pesel of student", default=None, required=False)
        parser.add_argument("--album", "-a", type=str, help="album number of student", default=None, required=False)

    def run(self):
        fname = self.app.args.firstname
        lname = self.app.args.lastname
        pesel = self.app.args.pesel
        album = self.app.args.album
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.get_student_completed_courses, fname, lname, pesel, album)
            print(DataFrame(result))


class CompleteCourse(Command):
    @staticmethod
    def register_arguments(parser):
        parser.add_argument("--student_nr", "-s", type=str, help="student number", required=True)
        parser.add_argument("--course_n", "-c", type=str, help="name of corse", required=True)

    def run(self):
        student = self.app.args.student_nr
        course = self.app.args.course_n
        with self.app.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.complete_course, course, student)
            if result:
                print("Signing up successful")


class Syllabus(App):
    """Syllabus app."""
    def __init__(self):
        super().__init__()
        self.db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))

    def register_commands(self):
        self.add_command("student_info", GetStudentInfo)
        self.add_command("tutor_info", GetTutorInfo)
        self.add_command("tutors_courses", TutorsCourses)
        self.add_command("tutors_department", TutorsDepartment)
        self.add_command("tutors_who_teaches_many_subjects", TutorsWhoTeachesManySubject)
        self.add_command("required_subjects", RequiredSubjects)
        self.add_command("missing_required_subjects", MissingRequiredSubjects)
        self.add_command("faculty_subjects", FacultySubjects)
        self.add_command("students_in_subject", StudentsInSubject)
        self.add_command("courses_ava_for_student", CoursesAvailableForStudents)
        self.add_command("shortest_path", ShortestSubjectPath)
        self.add_command("add_student", AddStudent)
        self.add_command("add_tutor", AddTutor)
        self.add_command("get_students_attends", GetStudentsAttends)
        self.add_command("get_students_completed", GetStudentsCompleted)
        self.add_command("add_subject", AddSubject)
        self.add_command("sign_up",SignUp)
        self.add_command("complete_course",CompleteCourse)
        self.add_command("few_faculty_subjects",FewDapartmentsSubjects)



if __name__ == "__main__":
    app = Syllabus()
    app.run()

