from PyQt5 import QtCore, QtGui, QtWidgets
from .main_window_UI import Ui_MainWindow
from .Student_dialog import StudentDialog
from .add_student_dialog import AddStudentDialog
from .signed_up import SignUpDialog
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
        self.present_table(dialog.student_info, self.tableWidget)
        self.present_table(dialog.attends, self.tableWidget_2)
        self.present_table(dialog.completed, self.tableWidget_3)

        # self.label2 = QtWidgets.QLabel(self.groupBox)
        # self.label3 = QtWidgets.QLabel(self.groupBox)
        # self.gridLayout_3.addWidget(self.label2, 2 , 0, 1, 2)
        # self.gridLayout_3.addWidget(self.label3, 2 , 2, 1, 2)
        # self.label.setText("Student information:")
        # self.label2.setText("Attends:")
        # self.label3.setText("Completed:")
        # self.label2.setMaximumSize(QtCore.QSize(16777215, 20))
        # self.label3.setMaximumSize(QtCore.QSize(16777215, 20))


        # self.tableWidget2 = QtWidgets.QTableWidget(self.groupBox)
        # self.setup_table_widget(self.tableWidget2, "TableWidget2", 3, 0, 1, 2)
        # self.present_table(dialog.attends, self.tableWidget2)

        # self.tableWidget3 = QtWidgets.QTableWidget(self.groupBox)
        # self.setup_table_widget(self.tableWidget3, "TableWidget3", 3, 2, 1, 2)
        # self.present_table(dialog.completed, self.tableWidget3)


    def tutors_subjects_clicked(self):
        dialog = StudentDialog(self, db=self.db)
        dialog.exec_()
        self.present_table(dialog.result, self.tableWidget)

    def add_student_clicked(self):
        dialog = AddStudentDialog(self, db=self.db)
        dialog.exec_()


    def make_student_complete_clicked(self):
        pass

    def sign_student_clicked(self):
        dialog = SignUpDialog(self, db=self.db)
        dialog.exec_()


    def setup_table_widget(self, obj, name, a, b, c, d):
        obj.setObjectName(name)
        obj.setColumnCount(0)
        obj.setRowCount(0)
        self.gridLayout_3.addWidget(obj, a, b, c, d)

    def present_table(self, result, tableWidget):
        rows = len(result)
        columns = 0
        if rows > 0:
            columns = len(result[0].keys())
        
            tableWidget.setRowCount(rows)
            tableWidget.setColumnCount(columns)
            tableWidget.setHorizontalHeaderLabels(list(result[0].keys()))
            for row, item_list in enumerate(result):
                for col, key in enumerate(item_list):
                    newitem = QtWidgets.QTableWidgetItem(str(item_list[key]))
                    tableWidget.setItem(row, col, newitem)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))
    form = MainWindow(db)
    form.show()
    app.exec_()





