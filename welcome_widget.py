"""
Logan Isitt
lai12
"""
from PyQt4 import QtGui, QtCore, Qt
from parse_rest.connection import register
from parse_rest.user import User

class WelcomeWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(WelcomeWidget, self).__init__()
        self.parent = parent
        register("c1gfGyShjoMC7Jdt9kGp5jOjKjUifPKN38H6Sak8", "0e9fGgFHK6Dw7Sh0S4SE6YW9t6Z61KMP7YQWl5DN")
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)
        username_lbl = QtGui.QLabel("Username:")
        password_lbl = QtGui.QLabel("Password:")

        self.username_field = QtGui.QLineEdit(self)
        self.password_field = QtGui.QLineEdit(self)

        self.grid.addWidget(username_lbl, 0, 0)
        self.grid.addWidget(self.username_field, 0, 1)

        self.grid.addWidget(password_lbl, 1, 0)
        self.grid.addWidget(self.password_field, 1, 1)

        self.login_btn = QtGui.QPushButton("Login")
        self.login_btn.clicked.connect(self.loginAction)
        self.grid.addWidget(self.login_btn, 2, 0, 1, 2)

        self.sign_up = QtGui.QPushButton("Sign up")
        self.sign_up.clicked.connect(self.signupAction)
        self.grid.addWidget(self.sign_up, 3, 0, 1, 2)

    def loginAction(self, event):
        un = str(self.username_field.text())
    	ps = str(self.password_field.text())
    	u = User.login(un, ps)
    	if (u is not None):
    	    self.parent.loggedInUser(u)

    def signupAction(self, event):
    	self.sign_up_window = SignUpWindow(self)
        self.sign_up_window.show()

class SignUpWindow(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(SignUpWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout() 
        self.setLayout(self.grid)

        username_lbl = QtGui.QLabel("Username:")
        password_lbl = QtGui.QLabel("Password:")

        self.username_field = QtGui.QLineEdit(self)
        self.password_field = QtGui.QLineEdit(self)

        first_name_lbl = QtGui.QLabel("First Name:")
        last_name_lbl = QtGui.QLabel("Last Name:")

        self.first_name_field = QtGui.QLineEdit(self)
        self.last_name_field = QtGui.QLineEdit(self)

        self.sign_up = QtGui.QPushButton("Submit")
        self.sign_up.clicked.connect(self.submit)

        self.grid.addWidget(username_lbl, 0, 0)
        self.grid.addWidget(self.username_field, 0, 1)

        self.grid.addWidget(password_lbl, 1, 0)
        self.grid.addWidget(self.password_field, 1, 1)

        self.grid.addWidget(first_name_lbl, 2, 0)
        self.grid.addWidget(self.first_name_field, 2, 1)

        self.grid.addWidget(last_name_lbl, 3, 0)
        self.grid.addWidget(self.last_name_field, 3, 1)

        self.grid.addWidget(self.sign_up, 4, 0, 1, 2)

        self.setWindowTitle('Sign Up')

    def submit(self, event):
    	un = str(self.username_field.text())
    	ps = str(self.password_field.text())
    	fn = str(self.first_name_field.text())
    	ln = str(self.last_name_field.text())

    	# Empty fields check

    	u = User.signup(un, ps, firstname=fn, lastname=ln)
    	if (u is not None):
    	    self.close()





