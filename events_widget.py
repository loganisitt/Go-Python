"""
Logan Isitt
lai12
"""
import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QDateTimeEdit
from PyQt4.QtCore import QDateTime

from event_model import Event

class EventsWidget(QtGui.QWidget):
    def __init__(self, parent, user):
        super(EventsWidget, self).__init__()
        self.parent = parent
        self.user = user
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)
        events_lbl = QtGui.QLabel("Events")

        self.create_btn = QtGui.QPushButton("Create Event")
        self.create_btn.clicked.connect(self.createEventAction)

        self.grid.addWidget(events_lbl, 0, 0)
        self.grid.addWidget(self.create_btn, 0, 3)

        self.events_list = QtGui.QWidget(self)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(EventsList(self, self.user))
        scroll.setWidgetResizable(True)

        self.grid.addWidget(scroll, 1, 0, 4, 4)

    def createEventAction(self, event):
        self.create_dialog = CreateDialog(self, self.user)
        self.create_dialog.show()

class EventsList(QtGui.QWidget):
    def __init__(self, parent, user):
        super(EventsList, self).__init__()
        self.parent = parent
        self.user = user
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)

        all_events = Event.Query.all()

        name_lbl = QtGui.QLabel("Name")
        date_lbl = QtGui.QLabel("Date")
        atts_lbl = QtGui.QLabel("Attendees")
        self.grid.addWidget(name_lbl, 0, 1)
        self.grid.addWidget(date_lbl, 0, 2)
        self.grid.addWidget(atts_lbl, 0, 3)

        for idx, event in enumerate(all_events):
            name_lbl = QtGui.QLabel(event.name)
            date_lbl = QtGui.QLabel(str(event.date))
            atts_lbl = QtGui.QLabel(str(len(event.attendees)))
            self.grid.addWidget(name_lbl, idx + 1, 1)
            self.grid.addWidget(date_lbl, idx + 1, 2)
            self.grid.addWidget(atts_lbl, idx + 1, 3)

            view_btn = QtGui.QPushButton("View")
            self.grid.addWidget(view_btn, idx + 1, 0)

            if (self.user.objectId == event.owner.objectId):
                delete_btn = QtGui.QPushButton("Delete")
                self.grid.addWidget(delete_btn, idx + 1, 4)

class CreateDialog(QtGui.QDialog):
    
    def __init__(self, parent, user):
        super(CreateDialog, self).__init__(parent)
        self.user = user
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)

        name_lbl = QtGui.QLabel("Name")
        desc_lbl = QtGui.QLabel("Description")
        time_lbl = QtGui.QLabel("Time")

        self.name_field = QtGui.QLineEdit(self)
        self.desc_field = QtGui.QLineEdit(self)

        self.event_date_field = QDateTimeEdit(QDateTime.currentDateTime())

        self.submit_btn = QtGui.QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit)

        self.grid.addWidget(name_lbl, 0, 0)
        self.grid.addWidget(self.name_field, 0, 1)

        self.grid.addWidget(desc_lbl, 1, 0, 1, 2)
        self.grid.addWidget(self.desc_field, 2, 0, 2, 2)

        self.grid.addWidget(time_lbl, 4, 0, 1, 2)
        self.grid.addWidget(self.event_date_field, 5, 0, 1, 2)

        self.grid.addWidget(self.submit_btn, 6, 0, 1, 2)

        self.setWindowTitle('Create Event')

    def submit(self, event):
        n = str(self.name_field.text())
        desc = str(self.desc_field.text())
        time = self.event_date_field.dateTime().toPyDateTime()
        e = Event(name=n, description=desc, owner=self.user, date=time, attendees=[self.user])
        e.save()
        self.close()
