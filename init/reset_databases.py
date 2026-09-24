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

DATABASES = [
    os.getenv("MYSQL_WAREHOUSE_DB", "hotel_warehouse"),
    os.getenv("MYSQL_TRANSACTIONAL_DB", "hotel_transactional"),
]


def reset_databases() -> None:
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        for database in DATABASES:
            cursor.execute(f"DROP DATABASE IF EXISTS `{database}`")
            print(f"Dropped database if it existed: {database}")

        connection.commit()

    except Error as error:
        print(f"Database reset failed: {error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    reset_databases()
