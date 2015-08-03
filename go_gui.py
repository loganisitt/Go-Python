"""
Logan Isitt
lai12
"""
import sys
from welcome_widget import *
from events_widget import *
from PyQt4 import QtGui, QtCore, Qt

class GoApp(QtGui.QMainWindow):
    def __init__(self):
        super(GoApp, self).__init__()
        self.initUI()

    def initUI(self):
        exitAction = QtGui.QAction('Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(app.quit)

        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        statbar = self.statusBar()

        self.welcome_widget = WelcomeWidget(self)
        self.setCentralWidget(self.welcome_widget)
    
        self.resize(200, 150)
        self.setWindowTitle('Go')
        self.show()

    def loggedInUser(self, user):
    	self.events_widget = EventsWidget(self, user)
        self.setCentralWidget(self.events_widget)
        self.resize(500, 200)
        self.center()

    def loggedOutUser(self):
    	self.welcome_widget = WelcomeWidget(self)
        self.setCentralWidget(self.welcome_widget)
        self.resize(200, 150)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):
    	event.accept()

app = QtGui.QApplication(sys.argv)
go_app = GoApp()
app.exec_()
