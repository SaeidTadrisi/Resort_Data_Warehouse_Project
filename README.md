# Resort Data Warehouse Pipeline

## Project Overview

This project focuses on the design and implementation of a complete Data Warehouse solution for a Resort Management System. The primary objective is to build a robust analytical infrastructure from an operational resort database to support managerial and strategic decision-making.

The project follows a modern **ELT (Extract, Load, Transform)** architecture, transforming highly normalized transactional data into a Star Schema optimized for Business Intelligence (BI).

---

## 🛠 Technology Stack

* **Data Generation:** Python (`Faker`, `mysql-connector-python`)
* **Database Engine:** MariaDB (Hosts both Operational DB and Analytical Data Warehouse)
* **Data Transformation:** dbt (Data Build Tool) - `dbt-core`, `dbt-mysql`
* **BI & Visualization:** Metabase (Dockerized / Local)

---

## 🏗 Architecture & Workflow

Our data pipeline flows through distinct conceptual and logical phases:

1. **Operational Source (Layer 1):** A highly normalized transactional database (`hotel_transactional`) simulating a real-world resort system. Data includes properties (Resorts, Hotels, Rooms) and transactions (Rentals, Services, Investments).
2. **Procedural Data Generation:** Python scripts embedded with business logic generate thousands of realistic records, accounting for seasonal demand, weekend spikes, and specific client behaviors.
3. 
**Analytical Warehouse (Layer 2):** Utilizing **dbt**, we extract raw tables, resolve complex many-to-many (M:N) relationships via reification, and transform them into a clean **Star Schema** (`hotel_warehouse`).


4. **BI Dashboard (Layer 3):** Metabase connects directly to the compiled dimensional models to answer complex decisional queries visually.

---

## 📊 Dimensional Modeling

Based on the decisional query analysis , the main business activities were identified as Facts for dimensional modeling .

| Fact Table | Business Process | Purpose / Key Measures |
| --- | --- | --- |
| `fact_room_rental` | Room Reservations 

 | Analyzes room revenue, rental duration, and booking volume.

 |
| `fact_rental_service` | Specific Service Usage 

 | Tracks wellness center service utilization and transaction revenue. |
| `fact_investment` | Investor Activity 

 | Monitors stock market title investments and value fluctuations. |

---

## 🚀 Installation & Setup Guide

### Prerequisites

* Python 3.8+
* MariaDB Server
* dbt-core

### Step 1: Database Setup

Execute the operational schema creation script to build the raw database (`hotel_transactional`):

```bash
python setup_database.py

```

### Step 2: Data Generation

Populate the operational database with simulated transactional data:

```bash
pip install -r requirements.txt
python generate_data.py

```

### Step 3: dbt Transformations

Configure your `~/.dbt/profiles.yml` to point to your local MariaDB instance. Then, navigate to the `hotel_dbt` directory to build the Star Schema (`hotel_warehouse`):

```bash
cd hotel_dbt
dbt deps
dbt run

```

### Step 4: Visualization

Connect your local Metabase instance to the `hotel_warehouse` database to explore the curated Fact and Dimension tables.

---
