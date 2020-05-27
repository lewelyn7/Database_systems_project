from PyQt5 import QtCore, QtGui, QtWidgets
from .signed_up_UI import Ui_Dialog
from ..db_helpers import DBHelpers
class SignUpDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(SignUpDialog, self).__init__()
        self.setupUi(self)
        self.db = kwargs['db']

    def OkClicked(self):
        album = self.lineEdit.text()
        subject = self.lineEdit_2.text()

        with self.db.driver1.session() as session:
            self.result = session.write_transaction(DBHelpers.sign_up, subject, album)

    def CancelClicked(self):
        pass