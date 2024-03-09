import pyodbc

def create_connection():
        
    # Replace these values with your SQL Server details
    server = 'LAPTOP-GPUVOBBI\SQLEXPRESS'
    database = 'SalaDeFitness'


    # Establish a connection
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'
    connection = pyodbc.connect(connection_string)

    return connection

