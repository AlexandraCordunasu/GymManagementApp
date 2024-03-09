from PyQt5.QtWidgets import QLabel, QSizePolicy, QHBoxLayout,QMessageBox,QComboBox,QFormLayout,QTableWidgetItem,QLineEdit, QTableWidget, QVBoxLayout, QPushButton,QWidget
import connection as conn
from PyQt5.QtGui import QFont
class AbonamenteSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 150,  # Nume Ctaegorie
            1: 100,  # Pret
            2: 100   # Durata
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)

    def __init__(self):
        super(AbonamenteSection, self).__init__()

        abonamente_section_layout = QVBoxLayout()
        self.original_id_abonament = None

        # Add widgets for Abonamente section
        two_rows_layout = QHBoxLayout()

        form_layout_row1 = QFormLayout()
        self.id_categorie_combobox = QComboBox()
        self.populate_categories()  # Populate the combo box with category names
        nume_categorie_label = QLabel("Nume Categorie:")
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        nume_categorie_label.setFont(font)
        form_layout_row1.addRow(nume_categorie_label, self.id_categorie_combobox)

        self.pret_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Pret:", "pret_input")
        self.durata_input = QLineEdit()
        self.add_form_field(form_layout_row1, "Durata:", "durata_input")
        two_rows_layout.addLayout(form_layout_row1)

        self.id_categorie_combobox.setMaximumWidth(200)
        self.pret_input.setMaximumWidth(200)
        self.durata_input.setMaximumWidth(200)

        abonamente_section_layout.addLayout(two_rows_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Assuming 4 columns for demonstration
        self.table.setHorizontalHeaderLabels(["Nume Categorie", "Pret", "Durata"])
        self.table.setMaximumHeight(300)
        self.table.setMaximumWidth(400)
        self.set_table_column_widths()

        abonamente_section_layout.addWidget(self.table)
        buttons_layout = QVBoxLayout()

        buttons_row1_layout = QHBoxLayout()
        # Button for Afiseaza
        afiseaza_button = QPushButton("Afiseaza Abonamentele")
        afiseaza_button.clicked.connect(self.afiseaza_function)
        self.style_button(afiseaza_button)

        # Button for Insert
        insert_button = QPushButton("Adauga Abonament Nou")
        insert_button.clicked.connect(self.insert_function)
        self.style_button(insert_button)

       

        buttons_row1_layout.addWidget(afiseaza_button)
        buttons_row1_layout.addWidget(insert_button)
        buttons_layout.addLayout(buttons_row1_layout)
        
        # A doua linie de butoane
        buttons_row2_layout = QHBoxLayout()
        # Button for Update
        update_button = QPushButton("Modifica Abonament")
        update_button.clicked.connect(self.update_function)
        self.style_button(update_button)

        # Button for Delete
        delete_button = QPushButton("Sterge Abonament")
        delete_button.clicked.connect(self.delete_function)
        self.style_button(delete_button)

        buttons_row2_layout.addWidget(update_button)
        buttons_row2_layout.addWidget(delete_button)

        buttons_layout.addLayout(buttons_row2_layout)

        button_font = QFont()
        button_font.setBold(True)
        afiseaza_button.setFont(button_font)
        insert_button.setFont(button_font)
        update_button.setFont(button_font)
        delete_button.setFont(button_font)

        abonamente_section_layout.addLayout(buttons_layout)

        self.setLayout(abonamente_section_layout)

        self.table.itemClicked.connect(self.table_item_clicked)

    def add_form_field(self, layout, label_text, label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10)  # Set the font size
        font.setBold(True)    # Set the font to bold
        label.setFont(font)
        input_field = QLineEdit()
        layout.addRow(label, input_field)
        setattr(self, label_name, input_field)

    def style_button(self, button):
        # Set button size policy to fixed, making it not stretch to fill available space
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Set width and height of the button
        button.setFixedSize(350, 60)
        # Set background color
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def afiseaza_function(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        query = """
        SELECT c.Nume_Categorie, a.Pret, a.Durata
        FROM Abonamente a
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

    def populate_categories(self):
        # Fetch category names from the database and populate the combo box
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()
        cursor.execute("SELECT nume_categorie FROM Categorie")
        categories = cursor.fetchall()
        self.id_categorie_combobox.addItems([category[0] for category in categories])
        conn_handle.close()

    def insert_function(self):
        if not all([
            self.id_categorie_combobox.currentText(),  # Check if a category is selected
            self.pret_input.text(),
            self.durata_input.text()
        ]):
            QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
            return

        # Connect to the database
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Fetch id_categorie based on the selected category name
        selected_category = self.id_categorie_combobox.currentText()
        query_category = "SELECT id_categorie FROM Categorie WHERE nume_categorie = ?"
        cursor.execute(query_category, (selected_category,))
        result = cursor.fetchone()

        if result is not None:
            id_categorie = result[0]

            # Execute the INSERT query with the fetched id_categorie
            query_insert = "INSERT INTO Abonamente (id_categorie, pret, durata) VALUES (?, ?, ?)"
            values_insert = (
                id_categorie,
                self.pret_input.text(),
                self.durata_input.text()
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
            QMessageBox.warning(self, "Warning", "Invalid category selected.")

    def clear_input_fields(self):
    # Clear all input fields after successful insertion
        self.id_categorie_combobox.setCurrentIndex(-1)  # Set the combo box to no selection
        self.pret_input.clear()
        self.durata_input.clear()
    def update_function(self):
    # Get the selected row index
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Get the values from the selected row
            id_categorie = self.table.item(selected_row, 0).text()
            pret = self.table.item(selected_row, 1).text()
            durata = self.table.item(selected_row, 2).text()

            # Check if the required fields are filled
            if not all([
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text()
            ]):
                QMessageBox.warning(self, "Warning", "All fields must be filled correctly.")
                return

            # Connect to the database
            conn_handle = conn.create_connection()
            cursor = conn_handle.cursor()

            # Fetch id_categorie based on the selected category name
            nume_categorie = self.table.item(selected_row, 0).text()
            query_category = "SELECT id_categorie FROM Categorie WHERE nume_categorie = ?"
            cursor.execute(query_category, (nume_categorie,))
            result = cursor.fetchone()

            if result is not None:
                id_categorie = result[0]

                # Execute the UPDATE query
                query_update = "UPDATE Abonamente SET pret=?, durata=? WHERE id_categorie=? AND pret=?"
                values_update = (
                    self.table.item(selected_row, 1).text(),
                    self.table.item(selected_row, 2).text(),
                    id_categorie,
                    pret
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
                QMessageBox.warning(self, "Warning", "Invalid category selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to update.")


    def delete_function(self):
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            conn_handle = conn.create_connection()

            cursor = conn_handle.cursor()

            # Retrieve the data from the selected row
            nume_categorie = self.table.item(selected_row, 0).text()
            pret = self.table.item(selected_row, 1).text()

            # Fetch id_categorie based on the selected category name
            query_category = "SELECT id_categorie FROM Categorie WHERE nume_categorie = ?"
            cursor.execute(query_category, (nume_categorie,))
            result = cursor.fetchone()

            if result is not None:
                id_categorie = result[0]

                values = ()
                query = "DELETE FROM Abonamente WHERE id_categorie = ? AND pret = ?"
                
                values = (id_categorie, pret)

                cursor.execute(query, values)

                conn_handle.commit()
                conn_handle.close()

                self.afiseaza_function()
                print('Delete button clicked')
            else:
                QMessageBox.warning(self, "Warning", "Invalid category selected.")
        else:
            QMessageBox.warning(self, "Warning", "Select a row to delete.")

        
    
    def table_item_clicked(self, item):
    # Get the selected row index
        selected_row = item.row()

        # Set the original ID Abonament for later use
        self.original_id_abonament = self.table.item(selected_row, 0).text()

        # Populate the input fields with data from the selected row
        # Use setCurrentText to set the value of the QComboBox
        category_name = self.table.item(selected_row, 0).text()
        index = self.id_categorie_combobox.findText(category_name)
        
        if index != -1:
            self.id_categorie_combobox.setCurrentIndex(index)

        self.pret_input.setText(self.table.item(selected_row, 1).text())
        self.durata_input.setText(self.table.item(selected_row, 2).text())