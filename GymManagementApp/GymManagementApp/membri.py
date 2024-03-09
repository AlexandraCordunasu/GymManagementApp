from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton,QWidget, QSizePolicy
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox,QTableWidgetItem,QRadioButton, QDateEdit, QFormLayout, QHBoxLayout,QTableWidget)

import connection as conn
from PyQt5.QtGui import QFont



class MembriSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume
            1: 150,  # Prenume
            2: 120,  # Data Nasterii
            3: 100,  # Telefon
            4: 150,  # Email
            5: 120,  # Data inscriere
            6: 50    # Sex
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)

    def __init__(self):
        super(MembriSection, self).__init__()
        #imi creez interfata
        membri_section_layout = QVBoxLayout()

        self.original_nume = None
        self.original_prenume = None
        self.original_telefon = None

        two_rows_layout = QHBoxLayout()
        form_layout_row1 = QFormLayout()
        self.nume_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Nume:","nume_input")
        self.prenume_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Prenume:","prenume_input")
        self.telefon_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Telefon:","telefon_input")
        self.email_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Email:","email_input")
        two_rows_layout.addLayout(form_layout_row1)

        self.nume_input.setMaximumWidth(300)
        self.prenume_input.setMaximumWidth(300)
        self.telefon_input.setMaximumWidth(300)
        self.email_input.setMaximumWidth(300)
       
        form_layout_row2 = QFormLayout()
        sex_label = QLabel("Sex:")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        sex_label.setFont(font)
        self.sex_f_radio = QRadioButton("F")
        self.sex_m_radio = QRadioButton("M")
        form_layout_row2.addRow(sex_label, self.sex_f_radio)
        form_layout_row2.addRow(QLabel(""), self.sex_m_radio)
        two_rows_layout.addLayout(form_layout_row2)

        self.data_nasterii_input = QDateEdit()
        self.add_date_selector(form_layout_row1, "Data Nasterii:", "data_nasterii_input")

        self.data_inscriere_input = QDateEdit()
        self.add_date_selector(form_layout_row1, "Data Inscriere:", "data_inscriere_input")

        self.data_nasterii_input.setFixedWidth(150)
        self.data_inscriere_input.setFixedWidth(150)
        
        membri_section_layout.addLayout(two_rows_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(7)  
        self.table.setHorizontalHeaderLabels(["Nume", "Prenume", "Data Nasterii","Telefon", "Email","Data inscriere", "Sex"])
        self.table.setMaximumHeight(250)
        self.table.setMaximumWidth(870)
        self.set_table_column_widths()
        membri_section_layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
       
        afiseaza_button = QPushButton("Afiseaza membrii")
        self.style_button(afiseaza_button)
        afiseaza_button.clicked.connect(self.afiseaza_function)

        insert_button = QPushButton("Adauga membru nou")
        insert_button.clicked.connect(self.insert_function)
        self.style_button(insert_button)

        update_button = QPushButton("Modifica membru")
        update_button.clicked.connect(self.update_function)
        self.style_button(update_button)

        delete_button = QPushButton("Sterge membru")
        delete_button.clicked.connect(self.delete_function)
        self.style_button(delete_button)

        button_font = QFont()
        button_font.setBold(True)

        afiseaza_button.setFont(button_font)
        insert_button.setFont(button_font)
        update_button.setFont(button_font)
        delete_button.setFont(button_font)
        
        buttons_layout.addWidget(afiseaza_button)
        buttons_layout.addWidget(insert_button)
        buttons_layout.addWidget(update_button)
        buttons_layout.addWidget(delete_button)

        membri_section_layout.addLayout(buttons_layout)
        self.setLayout(membri_section_layout)
        self.table.itemClicked.connect(self.table_item_clicked)

    def style_button(self, button):
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(180, 50)
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def add_form_field(self, layout, label_text,label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        label.setFont(font)
        input_field = QLineEdit()
        layout.addRow(label, input_field)
        setattr(self, label_name, input_field)
        
    def add_date_selector(self, layout, label_text,label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        label.setFont(font)
        date_selector = QDateEdit()
        layout.addRow(label, date_selector)
        setattr(self, label_name, date_selector)

    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()
        cursor.execute("SELECT Nume,Prenume,Data_Nasterii,Telefon,Email,Data_inscriere,Sex FROM Membri")
        data = cursor.fetchall()
        self.populate_table(data)
        conn_handle.close()
        print('Afiseaza button clicked')

    def populate_table(self, data):
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_value in enumerate(row_data):
                item = QTableWidgetItem(str(column_value))
                self.table.setItem(row_number, column_number, item)
        self.set_table_column_widths()

    def insert_function(self):
        if not all([
            self.nume_input.text(),
            self.prenume_input.text(),
            self.telefon_input.text(),
            self.email_input.text(),
            any([self.sex_f_radio.isChecked(), self.sex_m_radio.isChecked()]),
            self.data_nasterii_input.date().isValid(),
            self.data_inscriere_input.date().isValid()

        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor() 
        values = ()
        query = "INSERT INTO Membri (Nume, Prenume, Data_Nasterii, Telefon, Email, Data_inscriere,Sex ) VALUES (?, ?, ?, ?, ?, ?,?)"
        print("Data Nasterii:", self.data_nasterii_input.date().toString("yyyy-MM-dd HH:mm:ss"))
        print("Data Inscriere:", self.data_inscriere_input.date().toString("yyyy-MM-dd HH:mm:ss"))
        values = (
            self.nume_input.text(),
            self.prenume_input.text(),
            self.data_nasterii_input.date().toString("yyyy-MM-dd"),
            self.telefon_input.text(),
            self.email_input.text(),
            self.data_inscriere_input.date().toString("yyyy-MM-dd"),
            self.get_selected_sex()
        ) 
        cursor.execute(query, values)
        conn_handle.commit()
        conn_handle.close()
        self.clear_input_fields()
        self.afiseaza_function()
        print('Insert button clicked')

    def get_selected_sex(self):
        if self.sex_f_radio.isChecked():
            return "F"
        elif self.sex_m_radio.isChecked():
            return "M"

    def clear_input_fields(self):
        self.nume_input.clear()
        self.prenume_input.clear()
        self.telefon_input.clear()
        self.email_input.clear()
        self.sex_f_radio.setChecked(False)
        self.sex_m_radio.setChecked(False)
        self.data_nasterii_input.clear()
        self.data_inscriere_input.clear()

    def populate_fields_from_table(self, row):
        self.original_nume = self.table.item(row, 0).text()
        self.original_prenume = self.table.item(row, 1).text()
        self.original_telefon = self.table.item(row, 3).text()

    def table_item_clicked(self, item):
        selected_row = item.row()
        self.populate_fields_from_table(selected_row)

    def update_function(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            if not all([
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 3).text(),
                self.table.item(selected_row, 4).text()
            ]):
                QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
                return
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()
            print( self.table.item(selected_row, 0).text())
            query = "UPDATE Membri SET Nume=?, Prenume=?, Telefon=?, Email=? WHERE Nume=? AND Prenume=? AND Telefon=?"
            values = (
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 3).text(),
                self.table.item(selected_row, 4).text(),
                self.original_nume,
                self.original_prenume,
                self.original_telefon
            )
            cursor.execute(query, values)
            print( self.table.item(selected_row, 0).text())
            conn_handle.commit()
            conn_handle.close()
            self.clear_input_fields()
            self.afiseaza_function()
            print('Update button clicked')
        else:
            QMessageBox.warning(self, "Warning", "Select a row to update.")

    def delete_function(self):
        selected_row = self.table.currentRow()
        print(selected_row)
        
        if selected_row >= 0: 
            conn_handle = conn.create_connection()

            cursor = conn_handle.cursor() 
            nume = self.table.item(selected_row, 0).text()
            prenume = self.table.item(selected_row, 1).text()
            telefon = self.table.item(selected_row,3).text()

            values = ()
            query = "DELETE FROM Membri WHERE Nume = ? AND Prenume = ? AND Telefon = ?"
            
            values = (nume, prenume,telefon)

            cursor.execute(query, values)
           
            conn_handle.commit()
            conn_handle.close()

            self.afiseaza_function()            
            print('Delete button clicked')
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")
        