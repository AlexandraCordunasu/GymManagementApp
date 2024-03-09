import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QMessageBox, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton,QWidget
from membri import MembriSection
from antrenori import AntrenoriSection
from abonamente import AbonamenteSection
from clase import ClaseSection
from management import ManagementSection
from membriAbonamente import MembriiAbonamenteSection
from categorii import CategoriiSection
from membriClase import MembriClaseSection
import resources_rc
from PyQt5 import QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Admin Panel")

        membri_action = QtWidgets.QAction('Membri', self)
        membri_action.triggered.connect(self.showMembri)

        antrenori_action = QtWidgets.QAction('Antrenori', self)
        antrenori_action.triggered.connect(self.showAntrenori)

        clase_action = QtWidgets.QAction('Clase', self)
        clase_action.triggered.connect(self.showClase)

        abonamente_action = QtWidgets.QAction('Abonamente', self)
        abonamente_action.triggered.connect(self.showAbonamente)

        membriabonamente_action = QtWidgets.QAction('MembriiAbonamente', self)
        membriabonamente_action.triggered.connect(self.showMembriAbonamente)

        categorii_action = QtWidgets.QAction('Categorii', self)
        categorii_action.triggered.connect(self.showCategorii)

        membriclase_action = QtWidgets.QAction('Programari', self)
        membriclase_action.triggered.connect(self.showMembriiClase)

        management_action = QtWidgets.QAction('Management', self)
        management_action.triggered.connect(self.showManagement)

        

        logout_action = QtWidgets.QAction('Exit', self)
        logout_action.triggered.connect(self.logout)

        toolbar = self.addToolBar('Toolbar')
        
        toolbar.addAction(membri_action)
        toolbar.addAction(antrenori_action)
        toolbar.addAction(clase_action)
        toolbar.addAction(abonamente_action)
        toolbar.addAction(categorii_action)
        toolbar.addAction(membriclase_action)
        toolbar.addAction(management_action)
        toolbar.addAction(membriabonamente_action)
        toolbar.addAction(logout_action)

        self.icon_size = QtCore.QSize(40, 40)
        toolbar.setIconSize(self.icon_size)

        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #00BFFF;  /* Set your desired background color */
                spacing: 10px;  /* Adjust spacing between items */
            }
            QToolBar QToolButton {
                padding: 8px;  /* Adjust padding */
                font-size: 16px;  /* Set font size */
                color: #FFFFFF;  /* Set text color */
            }
            QToolBar QToolButton:hover {
                background-color: #3BB9FF;  /* Set the background color on hover */
            }
        """)

        self.central_widget_stack = QtWidgets.QStackedWidget()

        main_page_widget = QtWidgets.QWidget()
        self.showMembri()
        self.central_widget_stack.addWidget(main_page_widget)
        self.setCentralWidget(self.central_widget_stack)

    def showMembri(self):
        membri_section = MembriSection()
        self.central_widget_stack.addWidget(membri_section)
        self.central_widget_stack.setCurrentWidget(membri_section)
        print('Showing Membri section')

    def showAntrenori(self):
        antrenori_section = AntrenoriSection()
        self.central_widget_stack.addWidget(antrenori_section)
        self.central_widget_stack.setCurrentWidget(antrenori_section)
        print('Showing Antrenori section')

    def showClase(self):
        clase_section = ClaseSection()
        self.central_widget_stack.addWidget(clase_section)
        self.central_widget_stack.setCurrentWidget(clase_section)
        print('Showing Clase section')

    def showAbonamente(self):
        abonamente_section = AbonamenteSection()
        self.central_widget_stack.addWidget(abonamente_section)
        self.central_widget_stack.setCurrentWidget(abonamente_section)
        print('Showing Abonamente section')

    def showManagement(self):
        management_section = ManagementSection()
        self.central_widget_stack.addWidget(management_section)
        self.central_widget_stack.setCurrentWidget(management_section)
    def showMembriAbonamente(self):
        membriabonamente_section = MembriiAbonamenteSection()
        self.central_widget_stack.addWidget(membriabonamente_section)
        self.central_widget_stack.setCurrentWidget(membriabonamente_section)
    
    def showMembriiClase(self):
        membriclase_section = MembriClaseSection()
        self.central_widget_stack.addWidget(membriclase_section)
        self.central_widget_stack.setCurrentWidget(membriclase_section)

    def showCategorii(self):
        categorii_section =  CategoriiSection()
        self.central_widget_stack.addWidget(categorii_section)
        self.central_widget_stack.setCurrentWidget(categorii_section)

    def logout(self):
        QtWidgets.QApplication.quit()
        print('Logout action')

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton_2.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email=self.username.text()
        password=self.password.text()
        if email == "admin" and password=="admin123":
            print("Successfully logged in with email: ", email, "and password:", password)
            main_window = MainWindow()
            widget.addWidget(main_window)
            widget.setCurrentIndex(widget.currentIndex()+1)
        elif email == "user" and password == "user123":
            print("Successfully logged in as user")
            main2_window = Main2Window()
            widget.addWidget(main2_window)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            QMessageBox.warning(self, "Warning", "Username sau parola invalide.")
    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("signup.ui",self)
        self.loginbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        email = self.username.text()
        if self.password.text()==self.password_2.text():
            password=self.password.text()
            print("Successfully created acc with email: ", email, "and password: ", password)
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

class Main2Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main2Window, self).__init__()

app=QApplication(sys.argv)
login_window=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(login_window)
widget.setFixedWidth(1100)
widget.setFixedHeight(600)
widget.show()
login_window.show()
app.exec_()



