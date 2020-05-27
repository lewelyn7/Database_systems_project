from PyQt5 import QtCore, QtGui, QtWidgets
from .Student_dialog_UI import Ui_DialogStudentInfo
from ..db_helpers import DBHelpers
class AddStudentDialog(QtWidgets.QDialog, Ui_DialogStudentInfo):

    def __init__(self, *args, **kwargs):
        super(AddStudentDialog, self).__init__()
        self.setupUi(self)
        self.db = kwargs['db']

    def OkClicked(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_2.text()
        pesel = self.lineEdit_4.text()
        album = self.lineEdit_3.text()

        if not fname:
            fname = ""
        if not lname:
            lname = ""
        if not album:
            album = ""
        if not pesel:
            pesel = ""

        with self.db.driver1.session() as session:
            result = session.write_transaction(DBHelpers.add_student, firstname=fname, lastname=lname, pesel=pesel, album_nr=album)
            if result == 0:
                self.label_info.setText("student has been added")
            elif result == -1:
                self.label_info.setText("ERROR: wrong input data")
            else:
                self.label_info.setText("ERROR: student already exits")


    def CancelClicked(self):
        pass