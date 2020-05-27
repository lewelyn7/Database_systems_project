# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Student_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogStudentInfo(object):
    def setupUi(self, DialogStudentInfo):
        self.DialogStudentInfo = DialogStudentInfo
        DialogStudentInfo.setObjectName("DialogStudentInfo")
        DialogStudentInfo.resize(404, 222)
        self.gridLayout = QtWidgets.QGridLayout(DialogStudentInfo)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(DialogStudentInfo)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(DialogStudentInfo)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(DialogStudentInfo)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(DialogStudentInfo)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(DialogStudentInfo)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(DialogStudentInfo)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(DialogStudentInfo)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(DialogStudentInfo)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogStudentInfo)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.label_info = QtWidgets.QLabel(DialogStudentInfo)
        self.label_info.setText("")
        self.label_info.setObjectName("label_info")
        self.gridLayout.addWidget(self.label_info, 5, 1, 1, 1)

        self.retranslateUi(DialogStudentInfo)
        # self.buttonBox.accepted.connect(DialogStudentInfo.accept)
        self.buttonBox.rejected.connect(DialogStudentInfo.reject)
        self.buttonBox.clicked['QAbstractButton*'].connect(DialogStudentInfo.OkClicked)
        self.buttonBox.clicked['QAbstractButton*'].connect(DialogStudentInfo.CancelClicked)
        QtCore.QMetaObject.connectSlotsByName(DialogStudentInfo)

    def retranslateUi(self, DialogStudentInfo):
        _translate = QtCore.QCoreApplication.translate
        DialogStudentInfo.setWindowTitle(_translate("DialogStudentInfo", "Dialog"))
        self.label.setText(_translate("DialogStudentInfo", "Firstname"))
        self.label_4.setText(_translate("DialogStudentInfo", "Pesel"))
        self.label_3.setText(_translate("DialogStudentInfo", "Album number"))
        self.label_2.setText(_translate("DialogStudentInfo", "Lastname"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogStudentInfo = QtWidgets.QDialog()
    ui = Ui_DialogStudentInfo()
    ui.setupUi(DialogStudentInfo)
    DialogStudentInfo.show()
    sys.exit(app.exec_())
