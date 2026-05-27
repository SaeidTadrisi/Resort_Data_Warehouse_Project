import mysql.connector
from mysql.connector import Error


def create_database_and_tables():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password=''
        )

        cursor = connection.cursor()

        sql_commands = [
            "CREATE DATABASE IF NOT EXISTS hotel_transactional;",
            "USE hotel_transactional;",

            """CREATE TABLE IF NOT EXISTS Person (
                CF VARCHAR(50) PRIMARY KEY, Name VARCHAR(100), Age INT,
                Gender VARCHAR(10), Address VARCHAR(255), City VARCHAR(100), Country VARCHAR(100)
            );""",

            """CREATE TABLE IF NOT EXISTS Resort (
                ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(100),
                Address VARCHAR(255), City VARCHAR(100), Country VARCHAR(100)
            );""",

            """CREATE TABLE IF NOT EXISTS Hotel (
                ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(100),
                Address VARCHAR(255), City VARCHAR(100), Country VARCHAR(100),
                Resort_ID INT, FOREIGN KEY (Resort_ID) REFERENCES Resort(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Room (
                ID INT AUTO_INCREMENT PRIMARY KEY, Size INT, Type VARCHAR(50),
                Price DECIMAL(10, 2), Hotel_ID INT, FOREIGN KEY (Hotel_ID) REFERENCES Hotel(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Wellness_Center (
                ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(100),
                Address VARCHAR(255), City VARCHAR(100), Country VARCHAR(100),
                Resort_ID INT, FOREIGN KEY (Resort_ID) REFERENCES Resort(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Specific_Service (
                ID INT AUTO_INCREMENT PRIMARY KEY, Type VARCHAR(100),
                Duration INT, Price DECIMAL(10, 2), Wellness_Center_ID INT,
                FOREIGN KEY (Wellness_Center_ID) REFERENCES Wellness_Center(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Stock_Market_Title (
                ID INT AUTO_INCREMENT PRIMARY KEY, Type VARCHAR(100)
            );""",

            """CREATE TABLE IF NOT EXISTS Rent (
                ID INT AUTO_INCREMENT PRIMARY KEY, CF VARCHAR(50), Room_ID INT,
                Rent_Date DATE, Period INT,
                FOREIGN KEY (CF) REFERENCES Person(CF), FOREIGN KEY (Room_ID) REFERENCES Room(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Rent_Service (
                ID INT AUTO_INCREMENT PRIMARY KEY, CF VARCHAR(50), Service_ID INT, Service_Date DATE,
                FOREIGN KEY (CF) REFERENCES Person(CF), FOREIGN KEY (Service_ID) REFERENCES Specific_Service(ID)
            );""",

            """CREATE TABLE IF NOT EXISTS Investment (
                ID INT AUTO_INCREMENT PRIMARY KEY, CF VARCHAR(50), Title_ID INT,
                Investment_Date DATE, Amount DECIMAL(15, 2), Duration INT,
                FOREIGN KEY (CF) REFERENCES Person(CF), FOREIGN KEY (Title_ID) REFERENCES Stock_Market_Title(ID)
            );"""
        ]

        for command in sql_commands:
            cursor.execute(command)

        print("Database and all tables has been created! ✅")

    except Error as e:
        print(f" Error in connection or code! ❌ {e}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_database_and_tables()