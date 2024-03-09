from PyQt5.QtWidgets import QLabel,QSizePolicy, QHBoxLayout, QMessageBox, QComboBox, QFormLayout, QTableWidgetItem,\
    QDateEdit, QTableWidget, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
import connection as conn
import re


class MembriiAbonamenteSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume
            1: 150,  # Prenume
            2: 150,  # Data Nasterii
            3: 150
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)
    def __init__(self):
        super(MembriiAbonamenteSection, self).__init__()

        membrii_abonamente_layout = QVBoxLayout()
        self.original_id_membrii_abonament = None

        start_layout = QVBoxLayout()

        # Adaugă textul și QComboBox-ul pentru antrenori
        start_label = QLabel("Afiseaza membrii care au cel mai scump abonament si lucreaza cu antrenorul:")
        self.antrenori_combobox = QComboBox()
        self.populate_antrenori()
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.antrenori_combobox)

        membrii_abonamente_layout.addLayout(start_layout)
        # Add widgets for Membrii Abonamente section
        two_rows_layout = QHBoxLayout()

        form_layout_row1 = QFormLayout()
        self.id_membru_combobox = QComboBox()
        self.populate_members()  # Populate the combo box with member names
        form_layout_row1.addRow("Nume Membru:", self.id_membru_combobox)

        
        self.id_abonament_combobox = QComboBox()  
        self.id_durata_abonament_combobox = QComboBox()
        self.populate_abonamente()  # Populate the combo box with abonament names
        form_layout_row1.addRow("Categorie: ", self.id_abonament_combobox)

        self.id_abonament_combobox.currentIndexChanged.connect(self.populate_durata)
        # self.populate_durata()  # Populate the combo box with abonament names
        form_layout_row1.addRow("Durata: ", self.id_durata_abonament_combobox)

        
        self.data_incepere_input = QDateEdit()
        form_layout_row1.addRow("Data Incepere:", self.data_incepere_input)

        self.data_sfarsit_input = QDateEdit()
        form_layout_row1.addRow("Data Sfarsit:", self.data_sfarsit_input)

        two_rows_layout.addLayout(form_layout_row1)

        membrii_abonamente_layout.addLayout(two_rows_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Assuming 4 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume Membru", "Nume Abonament", "Data Incepere", "Data Sfarsit"])
        self.table.setMaximumWidth(650)
        self.set_table_column_widths()
        membrii_abonamente_layout.addWidget(self.table)

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

        membrii_abonamente_layout.addLayout(buttons_layout)

        self.antrenori_combobox.currentIndexChanged.connect(self.afiseaza_function_custom)

        self.setLayout(membrii_abonamente_layout)

        self.table.itemClicked.connect(self.table_item_clicked)
    
    def style_button(self, button):
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(180, 50)
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def populate_antrenori(self):
        # Populează combo box-ul cu numele și prenumele antrenorilor din baza de date
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        cursor.execute("SELECT Nume, Prenume FROM Antrenor")
        antrenori = cursor.fetchall()
        self.antrenori_combobox.addItems([f"{antrenor[0]} {antrenor[1]}" for antrenor in antrenori])

        conn_handle.close()

    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Execute a JOIN query to fetch data from both MembriiAbonamente, Membrii, and Abonamente tables
        query = """
            SELECT m.Nume+' '+ m.Prenume, c.Nume_Categorie, ma.Data_incepere, ma.Data_sfarsit
            FROM MembriAbonamente ma
            JOIN Membri m ON ma.ID_Membru = m.ID_Membru
            JOIN Abonamente a ON ma.ID_Abonament = a.ID_Abonament
            JOIN Categorie c ON a.ID_Categorie = c.ID_Categorie
            """

        cursor.execute(query)
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

    def populate_members(self):
        # Fetch member names from the database and populate the combo box
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()
        cursor.execute("SELECT Nume + ' ' + Prenume FROM Membri")
        members = cursor.fetchall()
        self.id_membru_combobox.addItems([member[0] for member in members])
        conn_handle.close()

    def populate_abonamente(self):
    # Fetch abonament names from the database and populate the combo box
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        cursor.execute("SELECT Nume_Categorie FROM Categorie")
        categorii = cursor.fetchall()
        self.id_abonament_combobox.addItems([categorie[0] for categorie in categorii])

        conn_handle.close()

    def populate_durata(self):
        # Fetch abonament durations based on the selected abonament and populate the combo box
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        selected_abonament = self.id_abonament_combobox.currentText()

        # Fetch durations based on the selected abonament
        cursor.execute("""SELECT a.Durata FROM Abonamente a 
                       JOIN Categorie c ON a.ID_Categorie = c.ID_Categorie WHERE c.Nume_Categorie = ?""", (selected_abonament,))
        durate = cursor.fetchall()

        # Clear existing items in the second combo box
        self.id_durata_abonament_combobox.clear()

        # Add the fetched durations to the second combo box
        self.id_durata_abonament_combobox.addItems([durata[0] for durata in durate])

        conn_handle.close()

    def insert_function(self):
        if not all([
            self.id_membru_combobox.currentText(),
            self.id_abonament_combobox.currentText(),
            self.data_incepere_input.date(),
            self.data_sfarsit_input.date()
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
        selected_abonament = self.id_abonament_combobox.currentText()
        query_categorie = "SELECT ID_Categorie FROM Categorie WHERE Nume_Categorie = ?"
        cursor.execute(query_categorie, (selected_abonament,))
        result_categorie = cursor.fetchone()

        if result_member is not None and result_categorie is not None:
            id_membru = result_member[0]
            id_categorie = result_categorie[0]

            query_abonament = "SELECT ID_Abonament FROM Abonamente WHERE Id_Categorie = ?"
            cursor.execute(query_abonament, (id_categorie,))
            result_abonament = cursor.fetchone()
            if result_abonament is not None:
                id_abonament = result_abonament[0]

                # Execute the INSERT query with the fetched id_membru, id_categorie, and durata
                query_insert = "INSERT INTO MembriAbonamente (ID_Membru, ID_Abonament, Data_incepere, Data_sfarsit) " \
                            "VALUES (?, ?, ?, ?)"
                values_insert = (
                    id_membru,
                    id_abonament,
                    self.data_incepere_input.date().toString("yyyy-MM-dd"),
                    self.data_sfarsit_input.date().toString("yyyy-MM-dd")
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
                QMessageBox.warning(self, "Warning", "Invalid categori selected.")

        else:
            QMessageBox.warning(self, "Warning", "Invalid member or abonament selected.")


    def clear_input_fields(self):
        # Clear all input fields after successful insertion
        self.id_membru_combobox.setCurrentIndex(-1)  # Set the combo box to no selection
        self.id_abonament_combobox.setCurrentIndex(-1)
        self.data_incepere_input.setDate(QDate.currentDate())
        self.data_sfarsit_input.setDate(QDate.currentDate())

    def update_function(self):
        # Get the selected row index
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Get the values from the selected row
            nume_membru = self.id_membru_combobox.currentText()
            nume_abonament = self.id_abonament_combobox.currentText()
            data_incepere = self.data_incepere_input.date().toString("yyyy-MM-dd")
            data_sfarsit = self.data_sfarsit_input.date().toString("yyyy-MM-dd")

            # Check if the required fields are filled
            if not all([nume_membru, nume_abonament, data_incepere, data_sfarsit]):
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

            # Fetch id_abonament based on the selected abonament name
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

                # Execute the UPDATE query
                query_update = "UPDATE MembriAbonamente SET Data_incepere=?, Data_sfarsit=? " \
                               "WHERE ID_Membru=? AND ID_Abonament = ?"
                values_update = (
                    data_incepere,
                    data_sfarsit,
                    id_membru,
                    id_abonament
                )
                cursor.execute(query_update, values_update)

                # Commit the transaction and close the database connection
                conn_handle.commit()
                conn_handle.close()

                # Clear the input fields after successful update
                self.clear_input_fields()

                # Refresh the table to display the updated data
                self.afiseaza_function()
                print('Update button clicked')
            else:
                QMessageBox.warning(self, "Warning", "Invalid member or abonament selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to update.")

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

    def table_item_clicked(self, item):
        # Get the selected row index
        selected_row = item.row()

        # Set the original ID Membrii Abonament for later use
        self.original_id_membrii_abonament = self.table.item(selected_row, 0).text()

        # Populate the input fields with data from the selected row
        # Use setCurrentText to set the value of the QComboBox for membrii
        membrii_full_name = self.table.item(selected_row, 0).text()
        
        # Split the full name into Nume and Prenume
        nume_membrii, prenume_membrii = membrii_full_name.split(' ', 1)
        
        index_membrii = self.id_membru_combobox.findText(membrii_full_name)
        
        if index_membrii != -1:
            self.id_membru_combobox.setCurrentIndex(index_membrii)

        # Use setCurrentText to set the value of the QComboBox for abonamente
        abonament_name = self.table.item(selected_row, 1).text()
        index_abonament = self.id_abonament_combobox.findText(abonament_name)
        
        if index_abonament != -1:
            self.id_abonament_combobox.setCurrentIndex(index_abonament)

        # Get the date strings from the table
        data_incepere_str = self.table.item(selected_row, 2).text()
        data_sfarsit_str = self.table.item(selected_row, 3).text()

        # Convert the date strings to QDate objects and set them in the QDateEdit fields
        self.data_incepere_input.setDate(QDate.fromString(data_incepere_str, "yyyy-MM-dd"))
        self.data_sfarsit_input.setDate(QDate.fromString(data_sfarsit_str, "yyyy-MM-dd"))
    
    def afiseaza_function_custom(self):

        antrenor_full_name = self.antrenori_combobox.currentText()
        nume_antrenor, prenume_antrenor = antrenor_full_name.split(' ', 1)

        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Execute the custom query with specified antrenor name and surname
        query = f"""
            SELECT m.Nume + ' ' + m.Prenume as 'Nume membru', a.Pret, ant.Nume + ' ' + ant.Prenume as 'Nume antrenor'
            FROM Membri m 
            JOIN MembriAbonamente ma ON ma.Id_Membru = m.Id_Membru
            JOIN Abonamente a ON ma.ID_Abonament = a.ID_Abonament
            JOIN MembriClase mc ON m.Id_Membru = mc.ID_Membru
            JOIN Clase c ON mc.ID_Clasa = c.ID_Clasa
            JOIN Antrenor ant ON c.ID_Antrenor = ant.ID_Antrenor
            WHERE a.Pret IN (SELECT MAX(a2.Pret) FROM Abonamente a2)
            AND ant.Nume LIKE ? 
            AND ant.Prenume LIKE ?
        """

        cursor.execute(query, (f"%{nume_antrenor}%", f"%{prenume_antrenor}%"))
        data = cursor.fetchall()
        self.populate_table(data)

        conn_handle.close()
        print(f'Afiseaza membrii cu cel mai scump abonament si antrenorul {nume_antrenor} {prenume_antrenor} button clicked')
