import os
import random
from datetime import date, timedelta

import mysql.connector
from dotenv import load_dotenv
from faker import Faker
from mysql.connector import Error


load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3307")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}

TRANSACTIONAL_DB = os.getenv("MYSQL_TRANSACTIONAL_DB", "hotel_transactional")

SEED = 42
PERSON_COUNT = 300
RENTAL_COUNT = 1200
SERVICE_USAGE_COUNT = 700
INVESTMENT_COUNT = 400

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)


def reset_transactional_data(cursor) -> None:
    tables = [
        "investment",
        "rent_service",
        "rent",
        "specific_service",
        "wellness_center",
        "stock_market_title",
        "room",
        "hotel",
        "person",
        "resort",
    ]

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE `{table}`")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def insert_reference_data(cursor) -> tuple[list[str], list[int], list[int], list[int]]:
    resorts = [
        ("Palermo Resort", "Via Roma 1", "Palermo", "Italy"),
        ("Dutch Haven", "Dam Square 5", "Amsterdam", "Netherlands"),
        ("Algiers Oasis", "Rue Didouche 18", "Algiers", "Algeria"),
        ("Tokyo Zen", "Shibuya Crossing 1", "Tokyo", "Japan"),
    ]
    cursor.executemany(
        """
        INSERT INTO resort (name, address, city, country)
        VALUES (%s, %s, %s, %s)
        """,
        resorts,
    )

    cursor.execute("SELECT id, city, country FROM resort ORDER BY id")
    resort_rows = cursor.fetchall()

    hotels = [
        (
            f"{city} Grand Hotel",
            f"Central Avenue {resort_id}",
            city,
            country,
            resort_id,
        )
        for resort_id, city, country in resort_rows
    ]
    cursor.executemany(
        """
        INSERT INTO hotel (name, address, city, country, resort_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        hotels,
    )

    cursor.execute("SELECT id FROM hotel ORDER BY id")
    hotel_ids = [row[0] for row in cursor.fetchall()]

    room_templates = [
        ("Standard", 25, 95.00),
        ("Deluxe", 35, 145.00),
        ("Family Suite", 55, 220.00),
        ("Presidential Suite", 85, 420.00),
        ("Conference Room", 70, 300.00),
    ]
    rooms = []
    for hotel_id in hotel_ids:
        for room_type, size_sqm, nightly_rate in room_templates:
            rooms.extend(
                [
                    (size_sqm, room_type, nightly_rate, hotel_id),
                    (size_sqm, room_type, nightly_rate, hotel_id),
                ]
            )

    cursor.executemany(
        """
        INSERT INTO room (size_sqm, room_type, nightly_rate, hotel_id)
        VALUES (%s, %s, %s, %s)
        """,
        rooms,
    )

    cursor.execute("SELECT id FROM room ORDER BY id")
    room_ids = [row[0] for row in cursor.fetchall()]

    wellness_centers = [
        (
            "Sicily Wellness",
            "Via della Salute 8",
            "Palermo",
            "Italy",
            1,
        ),
        (
            "Tokyo Wellness",
            "Zen Street 12",
            "Tokyo",
            "Japan",
            4,
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO wellness_center (name, address, city, country, resort_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        wellness_centers,
    )

    cursor.execute("SELECT id FROM wellness_center ORDER BY id")
    wellness_center_ids = [row[0] for row in cursor.fetchall()]

    services = [
        ("Deep Tissue Massage", 60, 120.00, wellness_center_ids[0]),
        ("Facial Treatment", 45, 80.00, wellness_center_ids[0]),
        ("Yoga Session", 60, 35.00, wellness_center_ids[0]),
        ("Aromatherapy Massage", 60, 135.00, wellness_center_ids[1]),
        ("Meditation Session", 45, 30.00, wellness_center_ids[1]),
        ("Spa Package", 120, 210.00, wellness_center_ids[1]),
    ]
    cursor.executemany(
        """
        INSERT INTO specific_service
            (service_type, duration_minutes, price, wellness_center_id)
        VALUES (%s, %s, %s, %s)
        """,
        services,
    )

    cursor.execute("SELECT id FROM specific_service ORDER BY id")
    service_ids = [row[0] for row in cursor.fetchall()]

    investment_titles = [
        ("Real Estate",),
        ("Technology",),
        ("Sustainable Tourism",),
        ("Hospitality Bonds",),
    ]
    cursor.executemany(
        "INSERT INTO stock_market_title (title_type) VALUES (%s)",
        investment_titles,
    )

    cursor.execute("SELECT id FROM stock_market_title ORDER BY id")
    title_ids = [row[0] for row in cursor.fetchall()]

    people = []
    for _ in range(PERSON_COUNT):
        people.append(
            (
                fake.unique.ssn(),
                fake.name(),
                random.randint(18, 75),
                random.choice(["Female", "Male", "Non-binary"]),
                fake.street_address(),
                fake.city(),
                fake.country(),
            )
        )

    cursor.executemany(
        """
        INSERT INTO person
            (id, full_name, age, gender, address, city, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        people,
    )

    person_ids = [person[0] for person in people]
    return person_ids, room_ids, service_ids, title_ids


def random_date(start_date: date, end_date: date) -> date:
    duration = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, duration))


def insert_transactions(
    cursor,
    person_ids: list[str],
    room_ids: list[int],
    service_ids: list[int],
    title_ids: list[int],
) -> None:
    today = date.today()
    start_date = today - timedelta(days=4 * 365)

    rentals = [
        (
            random.choice(person_ids),
            random.choice(room_ids),
            random_date(start_date, today),
            random.randint(1, 14),
        )
        for _ in range(RENTAL_COUNT)
    ]
    cursor.executemany(
        """
        INSERT INTO rent (person_id, room_id, rent_date, period_days)
        VALUES (%s, %s, %s, %s)
        """,
        rentals,
    )

    service_usage = [
        (
            random.choice(person_ids),
            random.choice(service_ids),
            random_date(start_date, today),
        )
        for _ in range(SERVICE_USAGE_COUNT)
    ]
    cursor.executemany(
        """
        INSERT INTO rent_service (person_id, service_id, service_date)
        VALUES (%s, %s, %s)
        """,
        service_usage,
    )

    investments = [
        (
            random.choice(person_ids),
            random.choice(title_ids),
            random_date(start_date, today),
            round(random.uniform(1_000, 100_000), 2),
            random.randint(30, 730),
        )
        for _ in range(INVESTMENT_COUNT)
    ]
    cursor.executemany(
        """
        INSERT INTO investment
            (person_id, title_id, investment_date, amount, duration_days)
        VALUES (%s, %s, %s, %s, %s)
        """,
        investments,
    )


def print_row_counts(cursor) -> None:
    tables = [
        "resort",
        "hotel",
        "room",
        "wellness_center",
        "specific_service",
        "stock_market_title",
        "person",
        "rent",
        "rent_service",
        "investment",
    ]

    print(f"Generated data in {TRANSACTIONAL_DB}:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        print(f"- {table}: {cursor.fetchone()[0]}")


def generate_data() -> None:
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            database=TRANSACTIONAL_DB,
            **MYSQL_CONFIG,
        )
        cursor = connection.cursor()

        reset_transactional_data(cursor)
        person_ids, room_ids, service_ids, title_ids = insert_reference_data(cursor)
        insert_transactions(cursor, person_ids, room_ids, service_ids, title_ids)

        connection.commit()
        print_row_counts(cursor)

    except Error as error:
        if connection is not None:
            connection.rollback()
        print(f"Data generation failed: {error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    generate_data()
