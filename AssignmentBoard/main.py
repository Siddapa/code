import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QCheckBox, QLabel
from PyQt5.QtCore import QSize


class DailyItems:
    items = []

    def getItems(self):
        return self.items

    def addItem(self, newCheckBox, pos):
        self.items.append([newCheckBox, pos])

    def removeItem(self, itemPos):
        self.items.remove(self.items[itemPos])


def window():
    app = QApplication(sys.argv)

    w = QWidget()
    grid = QGridLayout()
    daily_items = DailyItems()
    w.setLayout(grid)

    daily_items_title = QLabel()
    daily_items_title.setText('Daily Items')
    daily_items_title.minimumSize()
    grid.addWidget(daily_items_title, 0, 0)

    new_box = QCheckBox()
    new_box.setText('amma')
    daily_items.addItem(new_box, (1, 0))

    for checkbox, pos in daily_items.getItems():
        grid.addWidget(checkbox, pos[0], pos[1])

    w.show()
    sys.exit(app.exec_())


window()
