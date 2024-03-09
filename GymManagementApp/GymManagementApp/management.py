from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton,QWidget, QSizePolicy
from PyQt5.QtWidgets import (QWidget,QComboBox, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox,QTableWidgetItem,QRadioButton, QDateEdit, QFormLayout, QHBoxLayout,QTableWidget)

import connection as conn
from PyQt5.QtGui import QFont

class ManagementSection(QWidget):
    def set_table_column_widths(self):
        column_widths = {
            0: 200,  # Nume
            1: 200,
            2: 200 # Prenume
        }
        for column, width in column_widths.items():
            self.table.setColumnWidth(column, width)
    def __init__(self):
        super(ManagementSection, self).__init__()

        management_layout = QVBoxLayout()

        # Button for executing the first query
        query_layout = QHBoxLayout()

# Adaugă un label pentru textul dorit
        query_label = QLabel("Afișează numărul de abonamente pentru fiecare categorie.")
        
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        query_label.setFont(font)
        query_layout.addWidget(query_label)
        # Adaugă butonul pentru a executa interogarea
        query_button1 = QPushButton("Afișează")
        query_button1.clicked.connect(self.execute_category_query)
        self.style_button(query_button1)
        query_layout.addWidget(query_button1)

        # Adaugă layout-ul vertical la layout-ul de management (înlocuiește cu numele layout-ului corespunzător)
        management_layout.addLayout(query_layout)

        # ...
        query_layout1 = QHBoxLayout()

        query_label1 = QLabel("Afișează categoriile care au cel puțin")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label1.setFont(font)
        query_layout1.addWidget(query_label1)

        self.min_count_input = QLineEdit()
        self.min_count_input.setPlaceholderText("Introduceți numărul")
        self.min_count_input.setMaximumWidth(100)
        query_layout1.addWidget(self.min_count_input)

        query_label2 = QLabel("de abonamente.")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label2.setFont(font)
        query_layout1.addWidget(query_label2)

        query_button1 = QPushButton("Afișează")
        query_button1.clicked.connect(self.numar_ales_abonamente)
        self.style_button(query_button1)
        query_layout1.addWidget(query_button1)

        management_layout.addLayout(query_layout1)
        query_layout2 = QHBoxLayout()

        query_label = QLabel("Afișează antrenorii cu cel mai mare număr de clase.")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label.setFont(font)
        query_layout2.addWidget(query_label)

        query_button2 = QPushButton("Afișează")
        query_button2.clicked.connect(self.numar_maxim_clase)
        self.style_button(query_button2)
        query_layout2.addWidget(query_button2)

        management_layout.addLayout(query_layout2)

        # Creează un layout orizontal pentru cele patru elemente
        query_layout4 = QHBoxLayout()

        # Adaugă QLabel-ul în layout-ul orizontal
        query_label4 = QLabel("Afișați clasele care au:")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label4.setFont(font)
        query_layout4.addWidget(query_label4)


        # Adaugă QComboBox-ul în layout-ul orizontal
        self.members_count_combo = QComboBox()
        self.members_count_combo.addItems(["cei mai mulți membrii", "cei mai puțini membrii"])
        query_layout4.addWidget(self.members_count_combo)

        # Adaugă QPushButton-ul în layout-ul orizontal
        query_button4 = QPushButton("Afișează")
        query_button4.clicked.connect(self.execute_class_query_membrii_multi_putini)
        self.style_button(query_button4)
        query_layout4.addWidget(query_button4)

        # Adaugă layout-ul orizontal în management_layout
        management_layout.addLayout(query_layout4)

        query_layout3 = QHBoxLayout()

        # Adaugă QLabel-ul în layout-ul orizontal
        query_label3 = QLabel("Afișează numărul de membri pentru fiecare clasă:")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label3.setFont(font)
        query_layout3.addWidget(query_label3)

        # Adaugă QPushButton-ul în layout-ul orizontal
        query_button3 = QPushButton("Afișează")
        query_button3.clicked.connect(self.execute_class_query_numar_membri)
        self.style_button(query_button3)
        query_layout3.addWidget(query_button3)

        # Adaugă layout-ul orizontal în management_layout
        management_layout.addLayout(query_layout3)

        query_layout5 = QHBoxLayout()

        # Adaugă QLabel-ul în layout-ul orizontal
        query_label5 = QLabel("Afișează numărul de abonamente pentru fiecare membru:")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        query_label5.setFont(font)
        query_layout5.addWidget(query_label5)

        # Adaugă QPushButton-ul în layout-ul orizontal
        query_button5 = QPushButton("Afișează")
        query_button5.clicked.connect(self.execute_member_abonamente_query)
        self.style_button(query_button5)
        query_layout5.addWidget(query_button5)

        # Adaugă layout-ul orizontal în management_layout
        management_layout.addLayout(query_layout5)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)  # Nume_Categorie și Numar_Abonamente
        self.result_table.setMaximumHeight(300)  # Adjust the value as needed
        self.result_table.setMaximumWidth(500)
        management_layout.addWidget(self.result_table)

        self.setLayout(management_layout)

    def style_button(self, button):
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(150, 40)
        button.setStyleSheet("background-color: #6666ff; color: black;")

    def add_form_field(self, layout, label_text,label_name):
        label = QLabel(label_text)
        font = QFont()
        font.setPointSize(10) 
        font.setBold(True)    
        label.setFont(font)
        input_field = QLineEdit()
        # layout.addRow(label, input_field)
        setattr(self, label_name, input_field)
    def execute_class_query_membrii_multi_putini(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # Obțineți valoarea selectată din meniul derulant
        selected_option = self.members_count_combo.currentText()

        if selected_option == "cei mai mulți membrii":
            query = """
                SELECT 
                    Clase.Numele_clasei,
                    COUNT(MembriClase.ID_Membru) AS Numar_membri_inscrisi
                FROM 
                    Clase
                LEFT JOIN 
                    MembriClase ON Clase.ID_Clasa = MembriClase.ID_Clasa
                GROUP BY 
                    Clase.ID_Clasa, Clase.Numele_clasei
                HAVING 
                    COUNT(MembriClase.ID_Membru) = (SELECT MAX(Numar_membri) 
                FROM (SELECT ID_Clasa, COUNT(ID_Membru) AS Numar_membri FROM MembriClase GROUP BY ID_Clasa) AS maxim);
                """
        else:
            query = """
            SELECT 
                Clase.Numele_clasei,
                COUNT(MembriClase.ID_Membru) AS Numar_membri_inscrisi
            FROM 
                Clase
            LEFT JOIN 
                MembriClase ON Clase.ID_Clasa = MembriClase.ID_Clasa
            GROUP BY 
                Clase.ID_Clasa, Clase.Numele_clasei
            HAVING 
                COUNT(MembriClase.ID_Membru) = (SELECT MIN(Numar_membri) FROM (SELECT ID_Clasa, COUNT(ID_Membru) AS Numar_membri FROM MembriClase 
                GROUP BY ID_Clasa) AS minim);
            """
        
        cursor.execute(query)
        data = cursor.fetchall()

        # Afișați rezultatele în tabela rezultatelor
        self.populate_result_table(data, ["Nume Clasa", "Numar Membri Inscrisi"])

        conn_handle.close()

    def execute_category_query(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # SQL Query
        query = """
            SELECT C.Nume_Categorie, COUNT(AM.ID_Abonament) AS Numar_Abonamente
            FROM Categorie C
            LEFT JOIN Abonamente A ON C.ID_Categorie = A.ID_Categorie
            JOIN MembriAbonamente AM ON A.ID_Abonament = AM.ID_Abonament
            GROUP BY C.ID_Categorie, C.Nume_Categorie
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Populate the result table with query results
        self.populate_result_table(data, ["Nume Categorie", "Numar Abonamente"])

        conn_handle.close()

    def numar_ales_abonamente(self):
        min_count = self.min_count_input.text()

        # Validate that the user has entered a valid integer
        try:
            min_count = int(min_count)
        except ValueError:
            print("Please enter a valid integer for the minimum count.")
            return

        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # SQL Query with HAVING clause
        query = f"""
            SELECT C.Nume_Categorie, COUNT(AM.ID_Abonament) AS Numar_Abonamente
            FROM Categorie C
            LEFT JOIN Abonamente A ON C.ID_Categorie = A.ID_Categorie
            JOIN MembriAbonamente AM ON A.ID_Abonament = AM.ID_Abonament
            GROUP BY C.ID_Categorie, C.Nume_Categorie
            HAVING COUNT(A.ID_Abonament) >= {min_count}
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Populate the result table with query results
        self.populate_result_table(data,["Nume Categorie", "Numar Abonamente"])

        conn_handle.close()
    

    def populate_result_table(self, data, column_names):
    # Clear existing data in the table
        self.result_table.setRowCount(0)

        # Set column names
        self.result_table.setHorizontalHeaderLabels(column_names)

        # Populate the table with the fetched data
        for row_number, row_data in enumerate(data):
            self.result_table.insertRow(row_number)
            for column_number, column_value in enumerate(row_data):
                item = QTableWidgetItem(str(column_value))
                self.result_table.setItem(row_number, column_number, item)

        # Adjust column widths based on content
        self.result_table.resizeColumnsToContents()
    
    def numar_maxim_clase(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # SQL Query
        query = """
            SELECT A.Nume, A.Prenume
            FROM Antrenor A
            WHERE A.ID_antrenor IN (
                SELECT Cl.ID_antrenor
                FROM Clase Cl
                GROUP BY Cl.ID_antrenor
                HAVING COUNT(Cl.ID_Clasa) = (
                    SELECT MAX(Numar_Clase) FROM (
                        SELECT COUNT(ID_Clasa) AS Numar_Clase
                        FROM Clase
                        GROUP BY ID_antrenor
                    ) AS SubQuery
                )
            )
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Populate the result table with query results
        self.populate_result_table(data, ["Nume Antrenor", "Prenume Antrenor"])

        conn_handle.close()

    def execute_class_query_numar_membri(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # SQL Query
        query = """
            SELECT Numele_clasei, 
                   (SELECT COUNT(*) 
                    FROM MembriClase 
                    WHERE MembriClase.ID_Clasa = Clase.ID_Clasa) AS Numar_Membri
            FROM Clase;
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Populate the result table with query results
        self.populate_result_table(data, ["Nume Clasa", "Numar Membri"])

        conn_handle.close()
    
    def execute_member_abonamente_query(self):
        conn_handle = conn.create_connection()
        cursor = conn_handle.cursor()

        # SQL Query
        query = """
            SELECT M.Nume, M.Prenume, AC.Numar_Abonamente
            FROM Membri M
            LEFT JOIN (
                SELECT ID_Membru, COUNT(ID_Abonament) AS Numar_Abonamente
                FROM MembriAbonamente
                GROUP BY ID_Membru
            ) AS AC ON M.ID_Membru = AC.ID_Membru;
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Populate the result table with query results
        self.populate_result_table(data, ["Nume", "Prenume", "Numar Abonamente"])

        conn_handle.close()