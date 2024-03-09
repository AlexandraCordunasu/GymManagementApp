from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QSizePolicy,
                             QCheckBox,QMessageBox,QTableWidgetItem,QRadioButton, QDateEdit, QFormLayout, QHBoxLayout,QTableWidget)
import connection as conn
from PyQt5.QtGui import QFont

class AntrenoriSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume
            1: 150,  # Prenume
            3: 100,  # Telefon
            4: 150,  # Email
            5: 150,  # CNP
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)

    def __init__(self):
        super(AntrenoriSection, self).__init__()

        antrenori_section_layout = QVBoxLayout()
        self.original_nume = None
        self.original_prenume = None
        self.original_cnp = None
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
        self.cnp_input = QLineEdit()
        self.add_form_field(form_layout_row1, "CNP:","cnp_input")
        two_rows_layout.addLayout(form_layout_row1)

        self.nume_input.setMaximumWidth(300)
        self.prenume_input.setMaximumWidth(300)
        self.telefon_input.setMaximumWidth(300)
        self.email_input.setMaximumWidth(300)
        self.cnp_input.setMaximumWidth(300)
       
        antrenori_section_layout.addLayout(two_rows_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Assuming 6 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume", "Prenume","Telefon", "Email", "CNP"])
        self.table.setMaximumWidth(720)
        self.set_table_column_widths()

        antrenori_section_layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
        # Button for Afiseaza
        afiseaza_button = QPushButton("Afiseaza Antrenorii")
        afiseaza_button.clicked.connect(self.afiseaza_function)
        self.style_button(afiseaza_button)

        # Button for Insert
        insert_button = QPushButton("Adauga antrenor nou")
        insert_button.clicked.connect(self.insert_function)
        self.style_button(insert_button)
        # Button for Update
        update_button = QPushButton("Modifica antrenor")
        update_button.clicked.connect(self.update_function)
        self.style_button(update_button)

        # Button for Delete
        delete_button = QPushButton("Sterge antrenor")
        delete_button.clicked.connect(self.delete_function)
        self.style_button(delete_button)

        # Add more widgets or customize as needed
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

        antrenori_section_layout.addLayout(buttons_layout)
        self.setLayout(antrenori_section_layout)

        
        self.table.itemClicked.connect(self.table_item_clicked)

    def style_button(self, button):
        # Set button size policy to fixed, making it not stretch to fill available space
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Set width and height of the button
        button.setFixedSize(150, 40)
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
        cursor.execute("SELECT Nume,Prenume,Telefon,Email,CNP FROM Antrenor")
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

        self.set_table_column_widths()
    def insert_function(self):
        if not all([
            self.nume_input.text(),
            self.prenume_input.text(),
            self.telefon_input.text(),
            self.email_input.text(),
            self.cnp_input.text()

        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor() # Replace with your actual connection function
        values = ()
        # Execute an INSERT query to add a new participant
        query = "INSERT INTO Antrenor (Nume, Prenume, Telefon, Email, CNP) VALUES (?, ?, ?, ?, ?)"
        
        values = (
            self.nume_input.text(),
            self.prenume_input.text(),
            self.telefon_input.text(),
            self.email_input.text(),
            self.cnp_input.text()

        )
# 
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
        self.prenume_input.clear()
        self.telefon_input.clear()
        self.email_input.clear()
        self.cnp_input.clear()
    
    def populate_fields_from_table(self, row):
        self.original_nume = self.table.item(row, 0).text()
        self.original_prenume = self.table.item(row, 1).text()
        self.original_cnp = self.table.item(row, 4).text()

    def table_item_clicked(self, item):
        # Get the selected row index
        selected_row = item.row()

        # Populate the input fields with data from the selected row
        self.populate_fields_from_table(selected_row)
    
    def update_function(self):
    # Get the selected row index
        selected_row = self.table.currentRow()
       
        if selected_row >= 0:
            # Get the values from the selected row
          
            
            # Check if the required fields are filled
            if not all([
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text(),
                self.table.item(selected_row, 3).text(),
                self.table.item(selected_row, 4).text()
            ]):
                QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
                return

            # Connect to the database
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()
            print( self.table.item(selected_row, 0).text())

            # Execute the UPDATE query
            query = "UPDATE Antrenor SET Nume=?, Prenume=?, Telefon=?, Email=?  WHERE Nume=? AND Prenume=? AND CNP=?"
            values = (
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text(),
                self.table.item(selected_row, 3).text(),
                self.original_nume,
                self.original_prenume,
                self.original_cnp
            )
            cursor.execute(query, values)
            print( self.table.item(selected_row, 0).text())
            # Commit the transaction and close the database connection
            conn_handle.commit()
            conn_handle.close()

            # Clear the input fields after successful update
            self.clear_input_fields()

            # Refresh the table to display the updated data
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
            # Retrieve the data from the selected row
            nume = self.table.item(selected_row, 0).text()
            prenume = self.table.item(selected_row, 1).text()
            telefon = self.table.item(selected_row,2).text()

            values = ()
            query = "DELETE FROM Antrenor WHERE Nume = ? AND Prenume = ? AND Telefon = ?"
            
            values = (nume, prenume,telefon)

            cursor.execute(query, values)
           
            conn_handle.commit()
            conn_handle.close()

            self.afiseaza_function()            
            print('Delete button clicked')
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")