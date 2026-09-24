import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3307")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}

TRANSACTIONAL_DB = os.getenv("MYSQL_TRANSACTIONAL_DB", "hotel_transactional")
WAREHOUSE_DB = os.getenv("MYSQL_WAREHOUSE_DB", "hotel_warehouse")


def create_databases_and_tables() -> None:
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{TRANSACTIONAL_DB}`")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{WAREHOUSE_DB}`")
        cursor.execute(f"USE `{TRANSACTIONAL_DB}`")

        statements = [
            """
            CREATE TABLE IF NOT EXISTS resort (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hotel (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL,
                resort_id INT NOT NULL,
                CONSTRAINT fk_hotel_resort
                    FOREIGN KEY (resort_id) REFERENCES resort(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS room (
                id INT AUTO_INCREMENT PRIMARY KEY,
                size_sqm INT NOT NULL,
                room_type VARCHAR(50) NOT NULL,
                nightly_rate DECIMAL(10, 2) NOT NULL,
                hotel_id INT NOT NULL,
                CONSTRAINT fk_room_hotel
                    FOREIGN KEY (hotel_id) REFERENCES hotel(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS person (
                id VARCHAR(50) PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS wellness_center (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL,
                resort_id INT NOT NULL,
                CONSTRAINT fk_wellness_center_resort
                    FOREIGN KEY (resort_id) REFERENCES resort(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS specific_service (
                id INT AUTO_INCREMENT PRIMARY KEY,
                service_type VARCHAR(100) NOT NULL,
                duration_minutes INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                wellness_center_id INT NOT NULL,
                CONSTRAINT fk_specific_service_wellness_center
                    FOREIGN KEY (wellness_center_id)
                    REFERENCES wellness_center(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stock_market_title (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title_type VARCHAR(100) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS rent (
                id INT AUTO_INCREMENT PRIMARY KEY,
                person_id VARCHAR(50) NOT NULL,
                room_id INT NOT NULL,
                rent_date DATE NOT NULL,
                period_days INT NOT NULL,
                CONSTRAINT fk_rent_person
                    FOREIGN KEY (person_id) REFERENCES person(id),
                CONSTRAINT fk_rent_room
                    FOREIGN KEY (room_id) REFERENCES room(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS rent_service (
                id INT AUTO_INCREMENT PRIMARY KEY,
                person_id VARCHAR(50) NOT NULL,
                service_id INT NOT NULL,
                service_date DATE NOT NULL,
                CONSTRAINT fk_rent_service_person
                    FOREIGN KEY (person_id) REFERENCES person(id),
                CONSTRAINT fk_rent_service_specific_service
                    FOREIGN KEY (service_id) REFERENCES specific_service(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS investment (
                id INT AUTO_INCREMENT PRIMARY KEY,
                person_id VARCHAR(50) NOT NULL,
                title_id INT NOT NULL,
                investment_date DATE NOT NULL,
                amount DECIMAL(15, 2) NOT NULL,
                duration_days INT NOT NULL,
                CONSTRAINT fk_investment_person
                    FOREIGN KEY (person_id) REFERENCES person(id),
                CONSTRAINT fk_investment_stock_market_title
                    FOREIGN KEY (title_id) REFERENCES stock_market_title(id)
            )
            """,
        ]

        for statement in statements:
            cursor.execute(statement)

        connection.commit()
        print(
            f"Created or verified databases: "
            f"{TRANSACTIONAL_DB}, {WAREHOUSE_DB}"
        )
        print(f"Created or verified tables in: {TRANSACTIONAL_DB}")

    except Error as error:
        print(f"Database setup failed: {error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_databases_and_tables()
