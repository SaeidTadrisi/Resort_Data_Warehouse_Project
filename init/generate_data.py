import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_fake_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='hotel_transactional'
        )
        cursor = conn.cursor()

        print("Removing old data")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        tables = ['Rent', 'Rent_Service', 'Investment', 'Person', 'Room', 'Hotel', 'Specific_Service', 'Wellness_Center', 'Stock_Market_Title', 'Resort']
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        print("1. Building strategic residences and hotels...")
        # Construction of residences based on the needs of project queries
        resorts_data = [
            ("Palermo Resort", "Via Roma 1", "Palermo", "Italy"),
            ("Dutch Haven", "Dam Square 5", "Amsterdam", "Netherlands"),
            ("Algiers Oasis", "Rue Didouche", "Algiers", "Algeria"),
            ("Tokyo Zen", "Shibuya Crossing", "Tokyo", "Japan")
        ]
        cursor.executemany("INSERT INTO Resort (Name, Address, City, Country) VALUES (%s, %s, %s, %s)", resorts_data)

        # Building a hotel for each residence
        for r_id in range(1, 5):
            cursor.execute("INSERT INTO Hotel (Name, Address, City, Country, Resort_ID) VALUES (%s, %s, %s, %s, %s)",
                           (f"Hotel {r_id}", "Same as Resort", "City", "Country", r_id))

        print("2. Building rooms and health services...")
        # Construction of various rooms (especially Family Suite and Conference Room, which are mentioned in the project form)
        room_types = ['Standard', 'Family Suite', 'Conference Room', 'Presidential']
        rooms_data = []
        for h_id in range(1, 5):
            for _ in range(10):
                rooms_data.append((random.randint(20, 150), random.choice(room_types), random.uniform(50.0, 500.0), h_id))
        cursor.executemany("INSERT INTO Room (Size, Type, Price, Hotel_ID) VALUES (%s, %s, %s, %s)", rooms_data)

        # Building health centers and services (such as Deep Tissue Massage)
        cursor.execute("INSERT INTO Wellness_Center (Name, Address, City, Country, Resort_ID) VALUES (%s, %s, %s, %s, %s)",
                       ("Sicily Wellness", "Palermo", "Palermo", "Italy", 1))
        services_data = [
            ("Deep Tissue Massage", 60, 120.00, 1),
            ("Facial Treatment", 45, 80.00, 1)
        ]
        cursor.executemany("INSERT INTO Specific_Service (Type, Duration, Price, Wellness_Center_ID) VALUES (%s, %s, %s, %s)", services_data)

        # Stock Building (Real Estate and Technology)
        cursor.executemany("INSERT INTO Stock_Market_Title (Type) VALUES (%s)", [("Real Estate",), ("Technology",)])

        print("3. Generating customers (Person)...")
        persons_data = []
        cfs = [] # Maintaining national codes for transaction registration
        for _ in range(200):
            cf = fake.unique.ssn()
            cfs.append(cf)
            persons_data.append((
                cf, fake.name(), random.randint(18, 75),
                random.choice(['Male', 'Female']), fake.street_address(),
                fake.city(), fake.country()
            ))
        cursor.executemany("INSERT INTO Person (CF, Name, Age, Gender, Address, City, Country) VALUES (%s, %s, %s, %s, %s, %s, %s)", persons_data)

        print("4. Recording reservations and financial transactions...")
        rents_data = []
        for _ in range(500):
            start_date = fake.date_between(start_date='-5y', end_date='today')
            rents_data.append((
                random.choice(cfs), random.randint(1, 40), start_date, random.randint(1, 15)
            ))
        cursor.executemany("INSERT INTO Rent (CF, Room_ID, Rent_Date, Period) VALUES (%s, %s, %s, %s)", rents_data)

        conn.commit()
        print("Data injection completed successfully! The raw database is now ready. ✅")

    except mysql.connector.Error as err:
        print(f": Error ❌ {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    generate_fake_data()