from methods_try import DBHelpers
from neo4j import GraphDatabase

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

class TableWidget(QWidget): 
    def __init__(self, spisok):
        super().__init__()

 

        table = QTableWidget()
        table.setRowCount(3)
        table.setColumnCount(3)

        vbox = QVBoxLayout(self)
        vbox.addWidget(table)

        for row, item_list in enumerate(spisok):
            for col, key in enumerate(item_list):
                newitem = QTableWidgetItem(item_list[key])
                table.setItem(row, col, newitem)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    db = DBHelpers("bolt://bazy.flemingo.ovh:7687", ("neo4j", "marcjansiwikania"))
    Alicje = []
    with db.driver1.session() as session:
        Alicje = session.write_transaction(DBHelpers.get_student_info, "Leszek")
    w = TableWidget(Alicje)
    w.show()
    sys.exit(app.exec_())