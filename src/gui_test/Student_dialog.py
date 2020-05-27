from PyQt5 import QtCore, QtGui, QtWidgets
from .Student_dialog_UI import Ui_DialogStudentInfo
from ..db_helpers import DBHelpers
class StudentDialog(QtWidgets.QDialog, Ui_DialogStudentInfo):

    def __init__(self, *args, **kwargs):
        super(StudentDialog, self).__init__()
        self.setupUi(self)
        self.db = kwargs['db']
        self.buttonBox.accepted.connect(self.DialogStudentInfo.accept)

    def OkClicked(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_2.text()
        pesel = self.lineEdit_4.text()
        album = self.lineEdit_3.text()

        if not fname:
            fname = None
        if not lname:
            lname = None
        if not album:
            album = None
        if not pesel:
            pesel = None

        with self.db.driver1.session() as session:
            self.student_info = session.write_transaction(DBHelpers.get_student_info, firstname=fname, lastname=lname, pesel=pesel, student_nr=album)
            self.completed = session.write_transaction(DBHelpers.get_student_completed_courses, firstname=fname, lastname=lname, pesel=pesel, student_nr=album)
            self.attends = session.write_transaction(DBHelpers.get_student_attends_courses, firstname=fname, lastname=lname, pesel=pesel, student_nr=album)

        return
    def CancelClicked(self):
        pass