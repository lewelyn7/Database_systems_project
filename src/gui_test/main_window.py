from PyQt5 import QtCore, QtGui, QtWidgets
from .main_window_UI import Ui_MainWindow
from .Student_dialog import StudentDialog
from ..db_helpers import DBHelpers
from os import sys
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, db):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.db = db
    def student_info_clicked(self):
        dialog = StudentDialog(self, db=self.db)
        dialog.exec_()
        self.present_table(dialog.result)

    def tutors_subjects_clicked(self):
        dialog = StudentDialog(self, db=self.db)
        dialog.exec_()
        self.present_table(dialog.result)

    def present_table(self, result):
        rows = len(result)
        columns = 0
        if rows > 0:
            columns = len(result[0].keys())
        
            self.tableWidget.setRowCount(rows)
            self.tableWidget.setColumnCount(columns)
            self.tableWidget.setHorizontalHeaderLabels(list(result[0].keys()))
            for row, item_list in enumerate(result):
                for col, key in enumerate(item_list):
                    newitem = QtWidgets.QTableWidgetItem(item_list[key])
                    self.tableWidget.setItem(row, col, newitem)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))
    form = MainWindow(db)
    form.show()
    app.exec_()





