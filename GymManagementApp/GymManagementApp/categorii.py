from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton,QWidget, QSizePolicy
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QCheckBox,QMessageBox,QTableWidgetItem,QRadioButton, QDateEdit, QFormLayout, QHBoxLayout,QTableWidget)

import connection as conn
from PyQt5.QtGui import QFont

class CategoriiSection(QWidget):
    def __init__(self):
        super(CategoriiSection, self).__init__()

        categorii_section_layout = QVBoxLayout()

        two_rows_layout = QHBoxLayout()

        form_layout_row1 = QFormLayout()
        self.nume_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Nume categorie:","nume_input")

        self.nume_input.setMaximumWidth(300)
        two_rows_layout.addLayout(form_layout_row1)

        categorii_section_layout.addLayout(two_rows_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(1)  # Assuming 6 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume categorie"])
        self.table.setMaximumWidth(400)
        categorii_section_layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
       
        afiseaza_button = QPushButton("Afiseaza categorie")
        afiseaza_button.clicked.connect(self.afiseaza_function)
        self.style_button(afiseaza_button)
        # membri_section_layout.addWidget(afiseaza_button)

        insert_button = QPushButton("Adauga categorie noua ")
        insert_button.clicked.connect(self.insert_function)
        self.style_button(insert_button)
        # membri_section_layout.addWidget(insert_button)

        delete_button = QPushButton("Sterge categoria")
        delete_button.clicked.connect(self.delete_function)
        self.style_button(delete_button)
        button_font = QFont()
        button_font.setBold(True)
        afiseaza_button.setFont(button_font)
        insert_button.setFont(button_font)
        delete_button.setFont(button_font)
        
        buttons_layout.addWidget(afiseaza_button)
        buttons_layout.addWidget(insert_button)
        buttons_layout.addWidget(delete_button)

        categorii_section_layout.addLayout(buttons_layout)
        
        self.setLayout(categorii_section_layout)

        
        
    
   
    def style_button(self, button):
        # Set button size policy to fixed, making it not stretch to fill available space
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Set width and height of the button
        button.setFixedSize(250, 60)
        # Set background color
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def add_form_field(self, layout, label_text,label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10)  # Set the font size
        font.setBold(True)    # Set the font to bold
        label.setFont(font)
        input_field = QLineEdit()
        layout.addRow(label, input_field)
        setattr(self, label_name, input_field)
    
    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()
        cursor.execute("SELECT Nume_Categorie FROM Categorie")
        data = cursor.fetchall()
        self.populate_table(data)
        conn_handle.close()
        print('Afiseaza button clicked')

    def populate_table(self, data):
        # Clear existing data in the table
        self.table.setRowCount(0)

        # Populate the table with the fetched data
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_value in enumerate(row_data):
                item = QTableWidgetItem(str(column_value))
                self.table.setItem(row_number, column_number, item)

        # Adjust column widths based on content
        self.table.resizeColumnsToContents()
    
    def insert_function(self):
        if not all([
            self.nume_input.text(),
        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor() 
        values = ()
        # Execute an INSERT query to add a new participant
        query = "INSERT INTO Categorie (Nume_Categorie) VALUES (?)"

        values = (
             self.nume_input.text()
        )
        cursor.execute(query, values)

        # Commit the transaction and close the database connection
        conn_handle.commit()
        conn_handle.close()

        # Clear the input fields after successful insertion
        self.clear_input_fields()

        # Refresh the table to display the updated data
        self.afiseaza_function()
        print('Insert button clicked')
    
    def clear_input_fields(self):
        # Clear all input fields after successful insertion
        self.nume_input.clear()
    
    def delete_function(self):
        selected_row = self.table.currentRow()
        print(selected_row)
        
        if selected_row >= 0: 
            conn_handle = conn.create_connection()

            cursor = conn_handle.cursor() 
            # Retrieve the data from the selected row
            nume = self.table.item(selected_row, 0).text()

            values = ()
            query = "DELETE FROM Categorie WHERE Nume_Categorie = ?"
            values = (nume)

            cursor.execute(query, values)
           
            conn_handle.commit()
            conn_handle.close()

            self.afiseaza_function()            
            print('Delete button clicked')
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")
        