from PyQt5.QtWidgets import QLabel,QSizePolicy, QHBoxLayout, QMessageBox, QComboBox, QFormLayout, \
    QTableWidgetItem, QLineEdit, QTimeEdit,QTableWidget, QVBoxLayout, QPushButton, QWidget
import connection as conn
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QFont



class ClaseSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume clasa
            1: 150,   # Ora inceperii
            2: 150,   # Numar locuri
            3: 150,   # Ora incheierii
            4: 150   # Nume antrenor
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)

    def __init__(self):
        super(ClaseSection, self).__init__()

        clase_section_layout = QVBoxLayout()
        self.original_id_clasa = None

        # Add widgets for Clase section
        two_rows_layout = QHBoxLayout()

        form_layout_row1 = QFormLayout()

        self.nume_clasa_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Nume Clasa:", "nume_clasa_input")
        
        self.ora_inceperii_input = QTimeEdit()  # Use QTimeEdit for time input
        self.add_form_field(form_layout_row1, "Ora Inceperii:", "ora_inceperii_input")
        
        self.numar_locuri_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Numar Locuri:", "numar_locuri_input")
        
        self.ora_incheierii_input = QTimeEdit()  # You may want to replace this with a QTimeEdit widget for time input
        self.add_form_field(form_layout_row1, "Ora Incheierii:", "ora_incheierii_input")
        
        self.nume_antrenor_combobox = QComboBox()  # Add a QComboBox for selecting antrenori
        self.populate_antrenori()  # Populate the combo box with antrenor names
        nume_antrenor_label = QLabel("Nume Antrenor:")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        nume_antrenor_label.setFont(font)
        form_layout_row1.addRow(nume_antrenor_label, self.nume_antrenor_combobox)
        
        two_rows_layout.addLayout(form_layout_row1)


        self.nume_clasa_input.setMaximumWidth(300)
        self.ora_inceperii_input.setMaximumWidth(100)
        self.numar_locuri_input.setMaximumWidth(100)
        self.ora_incheierii_input.setMaximumWidth(100)
        self.nume_antrenor_combobox.setMaximumWidth(300)
                                                    
        clase_section_layout.addLayout(two_rows_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Assuming 5 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume Clasa", "Ora Inceperii", "Numar Locuri", "Ora Incheierii", "Nume Antrenor", "Data"])
        self.table.setMaximumWidth(800)
        self.set_table_column_widths()


        clase_section_layout.addWidget(self.table)
        buttons_layout = QHBoxLayout()
        # Button for Afiseaza
        afiseaza_button = QPushButton("Afiseaza Clasele")
        afiseaza_button.clicked.connect(self.afiseaza_function)
        self.style_button(afiseaza_button)

        # Button for Insert
        insert_button = QPushButton("Adauga Clasa Noua")
        insert_button.clicked.connect(self.insert_function)
        self.style_button(insert_button)

        # Button for Update
        update_button = QPushButton("Modifica Clasa")
        update_button.clicked.connect(self.update_function)
        self.style_button(update_button)

        # Button for Delete
        delete_button = QPushButton("Sterge Clasa")
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

        clase_section_layout.addLayout(buttons_layout)

        self.setLayout(clase_section_layout)

        self.table.itemClicked.connect(self.table_item_clicked)

    def add_form_field(self, layout, label_text, label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10)  # Set the font size
        font.setBold(True)    # Set the font to bold
        label.setFont(font)
        input_field = QLineEdit() if "nume" in label_name else None
        if "ora_inceperii" in label_name or "ora_incheierii" in label_name:
            input_field = QTimeEdit()  # Use QTimeEdit for time input
        elif "numar_locuri" in label_name:
            input_field = QLineEdit()
            input_field.setValidator(QIntValidator()) 
        layout.addRow(label, input_field)
        setattr(self, label_name, input_field)

    def style_button(self, button):
        # Set button size policy to fixed, making it not stretch to fill available space
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Set width and height of the button
        button.setFixedSize(150, 40)
        # Set background color
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()


        query = """
        SELECT c.Numele_clasei, c.Ora_incepere, c.Numar_locuri, c.Ora_incheiere, a.Nume + ' ' + a.Prenume
        FROM Clase c
        JOIN Antrenor a ON c.ID_antrenor = a.ID_antrenor
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

    def populate_antrenori(self):
        # Fetch antrenor names from the database and populate the combo box
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()
        cursor.execute("SELECT CONCAT(Nume, ' ', Prenume) FROM Antrenor")
        antrenori = cursor.fetchall()
        self.nume_antrenor_combobox.addItems([antrenor[0] for antrenor in antrenori])
        conn_handle.close()

    def insert_function(self):
        if not all([
            self.nume_clasa_input.text(),
            self.ora_inceperii_input.text(),
            self.numar_locuri_input.text(),
            self.ora_incheierii_input.text(),
            self.nume_antrenor_combobox.currentText()  # Check if an antrenor is selected
        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return

        # Connect to the database
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Fetch id_antrenor based on the selected antrenor name
        selected_antrenor = self.nume_antrenor_combobox.currentText().split(' ')
        query_antrenor = "SELECT ID_antrenor FROM Antrenor WHERE Nume = ? AND Prenume = ?"
        cursor.execute(query_antrenor, (selected_antrenor[0], selected_antrenor[1]))
        result = cursor.fetchone()

        if result is not None:
            id_antrenor = result[0]

            # Execute the INSERT query with the fetched id_antrenor
            query_insert = "INSERT INTO Clase (ID_antrenor,.Numele_clasei, Ora_incepere, Numar_locuri, Ora_incheiere) " \
                           "VALUES (?, ?, ?, ?, ?)"
            values_insert = (
                id_antrenor,
                self.nume_clasa_input.text(),
                self.ora_inceperii_input.text(),
                self.numar_locuri_input.text(),
                self.ora_incheierii_input.text()
                
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
            QMessageBox.warning(self, "Warning", "Invalid antrenor selected.")

    def clear_input_fields(self):
        # Clear all input fields after successful insertion
        self.nume_clasa_input.clear()
        self.ora_inceperii_input.clear()
        self.numar_locuri_input.clear()
        self.ora_incheierii_input.clear()
        self.nume_antrenor_combobox.setCurrentIndex(-1)  # Set the combo box to no selection

    def update_function(self):
        # Get the selected row index
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Get the values from the selected row
            nume_clasa = self.nume_clasa_input.text()
            ora_inceperii = self.ora_inceperii_input.time().toString("hh:mm:ss")
            numar_locuri = self.numar_locuri_input.text()
            ora_incheierii = self.ora_incheierii_input.time().toString("hh:mm:ss")
            nume_antrenor = self.nume_antrenor_combobox.currentText()


            # Check if the required fields are filled
            if not all([nume_clasa, ora_inceperii, numar_locuri, ora_incheierii, nume_antrenor]):
                QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
                return


            # Connect to the database
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()

            # Fetch id_antrenor based on the selected antrenor name
            nume_antrenor = self.table.item(selected_row, 4).text()
            query_antrenor = "SELECT ID_antrenor FROM Antrenor WHERE CONCAT(Nume, ' ', Prenume) = ?"
            cursor.execute(query_antrenor, (nume_antrenor,))
            result = cursor.fetchone()

            if result is not None:
                id_antrenor = result[0]

                # Execute the UPDATE query
                query_update = "UPDATE Clase SET Ora_incepere=?, Numar_locuri=?, Ora_incheiere=?, ID_antrenor=? " \
                               "WHERE Numele_clasei=?"
                values_update = (
                    self.table.item(selected_row, 1).text(),
                    self.table.item(selected_row, 2).text(),
                    self.table.item(selected_row, 3).text(),
                    id_antrenor,
                    nume_clasa
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
                QMessageBox.warning(self, "Warning", "Invalid antrenor selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to update.")

    def delete_function(self):
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            conn_handle = conn.create_connection()

            cursor = conn_handle.cursor()

            # Retrieve the data from the selected row
            nume_clasa = self.table.item(selected_row, 0).text()
            ora_inceperii = self.table.item(selected_row, 1).text()

            # Fetch id_antrenor based on the selected antrenor name
            nume_antrenor = self.table.item(selected_row, 4).text()
            query_antrenor = "SELECT ID_antrenor FROM Antrenor WHERE CONCAT(Nume, ' ', Prenume) = ?"
            cursor.execute(query_antrenor, (nume_antrenor,))
            result = cursor.fetchone()

            if result is not None:
                id_antrenor = result[0]

                values = ()
                query = "DELETE FROM Clase WHERE Numele_clasei=? AND id_antrenor=?"
                values = (nume_clasa, id_antrenor)

                cursor.execute(query, values)

                conn_handle.commit()
                conn_handle.close()

                self.afiseaza_function()
                print('Delete button clicked')
            else:
                QMessageBox.warning(self, "Warning", "Invalid antrenor selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")

    def table_item_clicked(self, item):
        # Get the selected row index
        selected_row = item.row()

        # Set the original ID Clasa for later use
        self.original_id_clasa = self.table.item(selected_row, 0).text()

        # Populate the input fields with data from the selected row
        self.nume_clasa_input.setText(self.table.item(selected_row, 0).text())
       
        self.numar_locuri_input.setText(self.table.item(selected_row, 2).text())

        # Get the time strings from the table
        ora_inceperii_str = self.table.item(selected_row, 1).text()
        ora_incheierii_str = self.table.item(selected_row, 3).text()

        # Convert the time strings to QTime objects and set them in the QTimeEdit fields
        self.ora_inceperii_input.setTime(QTime.fromString(ora_inceperii_str, "hh:mm:ss"))
        self.ora_incheierii_input.setTime(QTime.fromString(ora_incheierii_str, "hh:mm:ss"))

        # Use setCurrentText to set the value of the QComboBox
        antrenor_name = self.table.item(selected_row, 4).text()
        index = self.nume_antrenor_combobox.findText(antrenor_name)

        if index != -1:
            self.nume_antrenor_combobox.setCurrentIndex(index)
