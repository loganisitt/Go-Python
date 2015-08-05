"""
Logan Isitt
lai12
"""
import sys
from functools import partial
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QDateTimeEdit
from PyQt4.QtCore import QDateTime

from parse_rest.user import User
from parse_rest.datatypes import Object

palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Background,QtCore.Qt.white)

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
        user_lbl = QtGui.QLabel(self.user.firstname + " " + self.user.lastname)

        self.create_btn = QtGui.QPushButton("Create Event")
        self.create_btn.clicked.connect(self.createEventAction)

        self.logout_btn = QtGui.QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logoutAction)

        self.grid.addWidget(events_lbl, 0, 0)
        self.grid.addWidget(self.create_btn, 0, 1)
        self.grid.addWidget(user_lbl, 0, 2)
        self.grid.addWidget(self.logout_btn, 0, 3)

        self.events_list = QtGui.QWidget(self)

        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(EventsList(self, self.user))
        self.scroll.setWidgetResizable(True)

        self.grid.addWidget(self.scroll, 1, 0, 4, 4)

    def createEventAction(self, event):
        self.create_dialog = CreateDialog(self, self.user)
        self.create_dialog.show()

    def logoutAction(self, event):
        self.parent.loggedOutUser()

    def updateEventList(self):
        self.scroll.setWidget(EventsList(self, self.user))
        
class EventsList(QtGui.QWidget):
    def __init__(self, parent, user):
        super(EventsList, self).__init__()
        self.parent = parent
        self.user = user
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)

        self.all_events = Event.Query.all()

        name_lbl = QtGui.QLabel("Name")
        date_lbl = QtGui.QLabel("Date")
        atts_lbl = QtGui.QLabel("Attendees")
        self.grid.addWidget(name_lbl, 0, 1)
        self.grid.addWidget(date_lbl, 0, 2)
        self.grid.addWidget(atts_lbl, 0, 3)

        for idx, event in enumerate(self.all_events):
            name_lbl = QtGui.QLabel(event.name)
            date_lbl = QtGui.QLabel(str(event.date))
            atts_lbl = QtGui.QLabel(str(len(event.attendees)))
            self.grid.addWidget(name_lbl, idx + 1, 1)
            self.grid.addWidget(date_lbl, idx + 1, 2)
            self.grid.addWidget(atts_lbl, idx + 1, 3)

            view_btn = QtGui.QPushButton("View")
            view_btn.clicked.connect(partial(self.viewEvent, event))
            self.grid.addWidget(view_btn, idx + 1, 0)

            if (self.user.objectId == event.owner.objectId):
                delete_btn = QtGui.QPushButton("Delete")
                delete_btn.clicked.connect(partial(self.deleteEvent, event))
                self.grid.addWidget(delete_btn, idx + 1, 4)

    def viewEvent(self, event):
        self.event_dialog = EventDialog(self, self.user, event)
        self.event_dialog.show()

    def deleteEvent(self, event):
        event.delete()
        self.parent.updateEventList()

class CreateDialog(QtGui.QDialog):
    
    def __init__(self, parent, user):
        super(CreateDialog, self).__init__(parent)
        self.user = user
        self.parent = parent
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
        self.parent.updateEventList()
        self.close()

class EventDialog(QtGui.QDialog):
    def __init__(self, parent, user, event):
        super(EventDialog, self).__init__(parent)
        self.user = user
        self.event = event
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)

        self.setWindowTitle(self.event.name)

        desc_lbl = QtGui.QLabel(self.event.description)
        date_lbl = QtGui.QLabel(str(self.event.date))
        atts_lbl = QtGui.QLabel("Attendees")

        self.grid.addWidget(date_lbl, 0, 0, 1, 2)
        self.grid.addWidget(desc_lbl, 1, 0, 1, 2)
        self.grid.addWidget(atts_lbl, 2, 0, 1, 2)

        self.attendees_list = QtGui.QWidget(self)
        self.atts_layout = QtGui.QGridLayout()
        self.attendees_list.setLayout(self.atts_layout)

        self.joined = False
        for idx, obj in enumerate(self.event.attendees):
            if (not self.joined and obj['objectId'] == self.user.objectId):
                self.joined = True
            user = User.Query.get(objectId=obj['objectId'])
            first_name_lbl = QtGui.QLabel(user.firstname)
            last_name_lbl = QtGui.QLabel(user.lastname)
            self.atts_layout.addWidget(first_name_lbl, idx, 0)
            self.atts_layout.addWidget(last_name_lbl, idx, 1)

        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.attendees_list)
        self.scroll.setWidgetResizable(True)

        self.grid.addWidget(self.scroll, 3, 0, 1, 2)

        if (self.joined):
            self.join_btn = QtGui.QPushButton("Leave")
        else: 
            self.join_btn = QtGui.QPushButton("Join")
        self.join_btn.clicked.connect(self.join)
        self.grid.addWidget(self.join_btn, 4, 0, 1, 2)

    def join(self, event):

        shouldAdd = True
        for idx, obj in enumerate(self.event.attendees):
            if (obj['objectId'] == self.user.objectId):
                shouldAdd = False
                self.event.attendees.remove(obj)

        if (shouldAdd):
            self.join_btn.setText("Leave")
            self.event.attendees.append(self.user)
        else:
            self.join_btn.setText("Join")
        self.event.save()

        self.event = Event.Query.get(objectId=self.event.objectId)

        self.attendees_list = QtGui.QWidget(self)
        self.atts_layout = QtGui.QGridLayout()
        self.attendees_list.setLayout(self.atts_layout)

        self.joined = False
        for idx, obj in enumerate(self.event.attendees):
            if (not self.joined and obj['objectId'] == self.user.objectId):
                self.joined = True
            user = User.Query.get(objectId=obj['objectId'])
            first_name_lbl = QtGui.QLabel(user.firstname)
            last_name_lbl = QtGui.QLabel(user.lastname)
            self.atts_layout.addWidget(first_name_lbl, idx, 0)
            self.atts_layout.addWidget(last_name_lbl, idx, 1)

        self.scroll.setWidget(self.attendees_list)

    def closeEvent(self, event):
        self.parent.parent.updateEventList()
        event.accept()

class Event(Object):
    pass