from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton,QWidget, QSizePolicy
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QComboBox,QCheckBox,QMessageBox,QTableWidgetItem,QRadioButton, QDateEdit, QFormLayout, QHBoxLayout,QTableWidget)

import connection as conn
from PyQt5.QtGui import QFont

class MembriClaseSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume Membru
            1: 50,   # Clasa
            2: 150   # Stare Programare
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)

    def __init__(self):
        super(MembriClaseSection, self).__init__()

        membrii_clase_layout = QVBoxLayout()
        two_rows_layout = QHBoxLayout()
        form_layout_row1 = QFormLayout()
        form_layout_row2 = QFormLayout()

        self.id_membru_combobox = QComboBox()
        self.populate_members()  # Populate the combo box with member names
        nume_membru_label = QLabel("Nume membru: ")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        nume_membru_label.setFont(font)
        form_layout_row1.addRow(nume_membru_label, self.id_membru_combobox)
        
        self.id_clasa_combobox = QComboBox()  
        self.populate_class()  # Populate the combo box with abonament names
        nume_clasa_label = QLabel("Clasa: ")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        nume_clasa_label.setFont(font)
        form_layout_row1.addRow(nume_clasa_label, self.id_clasa_combobox)

        self.id_stare=QComboBox()
        self.id_stare.addItem("Confirmata")
        self.id_stare.addItem("Neconfirmata")
        nume_stare_label = QLabel("Stare: ")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        nume_stare_label.setFont(font)
        form_layout_row1.addRow(nume_stare_label, self.id_stare)

        two_rows_layout.addLayout(form_layout_row1)
        # Adaugă textul și drop-down-ul în partea de sus a layout-ului
        
        text_label = QLabel("Afișează membrii care participă la clasa:")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        text_label.setFont(font)

        self.clase_combo = QComboBox()
        self.populate_clase_combo()  # Populează inițial drop-down-ul cu clasele existente
        form_layout_row2.addRow(text_label, self.clase_combo)
        
        two_rows_layout.addLayout(form_layout_row2)

        self.id_clasa_combobox.setMaximumWidth(200)
        self.id_membru_combobox.setMaximumWidth(200)
        self.id_stare.setMaximumWidth(200)
        self.clase_combo.setMaximumWidth(200)
        membrii_clase_layout.addLayout(two_rows_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Assuming 4 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume membru", "Clasa", "Stare programare"])
        self.table.setMaximumWidth(375)
        self.set_table_column_widths()
        membrii_clase_layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        # Button for Afiseaza
        afiseaza_button = QPushButton("Afiseaza programarii")
        self.style_button(afiseaza_button)
        afiseaza_button.clicked.connect(self.afiseaza_function)

        # Button for Insert
        insert_button = QPushButton("Adauga programari")
        self.style_button(insert_button)
        insert_button.clicked.connect(self.insert_function)

        # Button for Delete
        delete_button = QPushButton("Sterge programari")
        self.style_button(delete_button)
        delete_button.clicked.connect(self.delete_function)
        
        button_font = QFont()
        button_font.setBold(True)

        afiseaza_button.setFont(button_font)
        insert_button.setFont(button_font)
        delete_button.setFont(button_font)

        
        buttons_layout.addWidget(afiseaza_button)
        buttons_layout.addWidget(insert_button)
        buttons_layout.addWidget(delete_button)


        membrii_clase_layout.addLayout(buttons_layout)
        self.clase_combo.currentIndexChanged.connect(self.afiseaza_clasa_function)
        self.setLayout(membrii_clase_layout)

        self.table.itemClicked.connect(self.table_item_clicked)

    def style_button(self, button):
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(180, 50)
        button.setStyleSheet("background-color: #6666ff; color: black;")

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

    def populate_members(self):
            # Fetch member names from the database and populate the combo box
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()
            cursor.execute("SELECT Nume + ' ' + Prenume FROM Membri")
            members = cursor.fetchall()
            self.id_membru_combobox.addItems([member[0] for member in members])
            conn_handle.close()

    def populate_class(self):
        # Fetch abonament names from the database and populate the combo box
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()

            cursor.execute("SELECT Numele_clasei FROM Clase")
            categorii = cursor.fetchall()
            self.id_clasa_combobox.addItems([categorie[0] for categorie in categorii])

            conn_handle.close()
    def populate_clase_combo(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Obține numele claselor din baza de date
        query = "SELECT Numele_clasei FROM Clase"
        cursor.execute(query)
        data = cursor.fetchall()

        # Adaugă numele claselor în drop-down
        self.clase_combo.addItems([str(row[0]) for row in data])

        conn_handle.close()
    def clear_input_fields(self):
            # Clear all input fields after successful insertion
            self.id_membru_combobox.setCurrentIndex(0)  # Set the combo box to no selection
            self.id_clasa_combobox.setCurrentIndex(0)
            self.id_stare.setCurrentIndex(0)

    def table_item_clicked(self, item):
            # Get the selected row index
            selected_row = item.row()

            # Set the original ID Membrii Abonament for later use
            self.original_id_membrii_abonament = self.table.item(selected_row, 0).text()

            # Populate the input fields with data from the selected row
            # Use setCurrentText to set the value of the QComboBox for membrii
            membrii_full_name = self.table.item(selected_row, 0).text()
            
            # Split the full name into Nume and Prenume
            
            index_membrii = self.id_membru_combobox.findText(membrii_full_name)
            
            if index_membrii != -1:
                self.id_membru_combobox.setCurrentIndex(index_membrii)

            # Use setCurrentText to set the value of the QComboBox for abonamente
            abonament_name = self.table.item(selected_row, 1).text()
            index_abonament = self.id_clasa_combobox.findText(abonament_name)
            
            if index_abonament != -1:
                self.id_clasa_combobox.setCurrentIndex(index_abonament)

            # Get the date strings from the table
    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Execute a JOIN query to fetch data from both MembriiAbonamente, Membrii, and Abonamente tables
        query = """
            SELECT m.Nume + ' ' + m.Prenume, c.Numele_Clasei, mc.Stare_programare
            FROM MembriClase mc
            JOIN Membri m ON mc.ID_Membru = m.ID_Membru
            JOIN Clase c ON c.ID_Clasa = mc.ID_Clasa
            """

        cursor.execute(query)
        data = cursor.fetchall()
        self.populate_table(data)
        conn_handle.close()
        print('Afiseaza button clicked')
    
    def insert_function(self):
        if not all([
            self.id_membru_combobox.currentText(),
            self.id_clasa_combobox.currentText(),
            self.id_stare.currentText()
        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return

        # Connect to the database
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Fetch id_membru based on the selected member name
        selected_member = self.id_membru_combobox.currentText()
        query_member = "SELECT ID_Membru FROM Membri WHERE Nume + ' ' + Prenume = ?"
        cursor.execute(query_member, (selected_member,))
        result_member = cursor.fetchone()

        # Fetch id_categorie based on the selected abonament name
        selected_class = self.id_clasa_combobox.currentText()
        query_categorie = "SELECT ID_Clasa FROM Clase WHERE Numele_clasei = ?"
        cursor.execute(query_categorie, (selected_class,))
        result_clasa = cursor.fetchone()

        if result_member is not None and result_clasa is not None:
            id_membru = result_member[0]
            id_clasa = result_clasa[0]

            selected_option=self.id_stare.currentText()
                # Execute the INSERT query with the fetched id_membru, id_categorie, and durata
            query_insert = "INSERT INTO MembriClase (ID_Membru, ID_Clasa, Stare_programare) VALUES (?,?,?)"
                       
            values_insert = (
                    id_membru,
                    id_clasa,
                    selected_option
                    )

            cursor.execute(query_insert, values_insert)

                # Commit the transaction and close the database connection
            conn_handle.commit()
            conn_handle.close()

                # Clear the input fields after successful insertion
            self.clear_input_fields()

                # Refresh the table to display the updated data
            self.afiseaza_function()
            print('Insert button clicked')
        
        else:
            QMessageBox.warning(self, "Warning", "Invalid member or class selected.")
    def delete_function(self):
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()

            # Retrieve the data from the selected row
            nume_membru = self.table.item(selected_row, 0).text()
            nume_abonament = self.table.item(selected_row, 1).text()

            # Fetch id_membru based on the selected member name
            selected_member = self.id_membru_combobox.currentText()
            query_member = "SELECT ID_Membru FROM Membri WHERE Nume + ' ' + Prenume = ?"
            cursor.execute(query_member, (selected_member,))
            result_member = cursor.fetchone()

            query_categorie = "SELECT ID_Categorie FROM Categorie WHERE Nume_Categorie = ?"
            cursor.execute(query_categorie, (nume_abonament,))
            result_categorie = cursor.fetchone()
            # Fetch id_abonament based on the selected abonament name
            id_categorie = result_categorie[0]

            query_abonament = "SELECT ID_Abonament FROM Abonamente WHERE ID_Categorie = ?"
            cursor.execute(query_abonament, (id_categorie,))
            result_abonament = cursor.fetchone()

            if result_member is not None and result_abonament is not None:
                id_membru = result_member[0]
                id_abonament = result_abonament[0]

                # Execute the DELETE query
                query_delete = "DELETE FROM MembriAbonamente WHERE ID_Membru=? AND ID_Abonament=?"
                values_delete = (id_membru, id_abonament)
                cursor.execute(query_delete, values_delete)

                conn_handle.commit()
                conn_handle.close()

                self.afiseaza_function()
                print('Delete button clicked')
            else:
                QMessageBox.warning(self, "Warning", "Invalid member or abonament selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")
    
    def afiseaza_clasa_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Obțineți numele clasei introdus
        selected_clasa = self.clase_combo.currentText()
        # Execute the JOIN query to fetch data for the specific class
        query = f"""
            SELECT m.Nume + ' ' + m.Prenume, c.Numele_Clasei, mc.Stare_programare
            FROM MembriClase mc
            JOIN Membri m ON mc.ID_Membru = m.ID_Membru
            JOIN Clase c ON c.ID_Clasa = mc.ID_Clasa
            WHERE c.Numele_Clasei LIKE '%{selected_clasa}%'
        """

        cursor.execute(query)
        data = cursor.fetchall()
        self.populate_table(data)
        conn_handle.close()
        print('Afiseaza membrii pentru clasa specifica button clicked')
