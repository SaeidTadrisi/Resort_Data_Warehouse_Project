# Baseline Database Inventory

This file records the database state before the portfolio rebuild.
It contains table names, columns, and row counts only.

## `hotel_transactional`

### `hotel`

- Rows: 4
- Columns:
  - `ID` - `int(11)`
  - `Name` - `varchar(100)`
  - `Address` - `varchar(255)`
  - `City` - `varchar(100)`
  - `Country` - `varchar(100)`
  - `Resort_ID` - `int(11)`

### `investment`

- Rows: 0
- Columns:
  - `ID` - `int(11)`
  - `CF` - `varchar(50)`
  - `Title_ID` - `int(11)`
  - `Investment_Date` - `date`
  - `Amount` - `decimal(15,2)`
  - `Duration` - `int(11)`

### `person`

- Rows: 200
- Columns:
  - `CF` - `varchar(50)`
  - `Name` - `varchar(100)`
  - `Age` - `int(11)`
  - `Gender` - `varchar(10)`
  - `Address` - `varchar(255)`
  - `City` - `varchar(100)`
  - `Country` - `varchar(100)`

### `rent`

- Rows: 500
- Columns:
  - `ID` - `int(11)`
  - `CF` - `varchar(50)`
  - `Room_ID` - `int(11)`
  - `Rent_Date` - `date`
  - `Period` - `int(11)`

### `rent_service`

- Rows: 0
- Columns:
  - `ID` - `int(11)`
  - `CF` - `varchar(50)`
  - `Service_ID` - `int(11)`
  - `Service_Date` - `date`

### `resort`

- Rows: 4
- Columns:
  - `ID` - `int(11)`
  - `Name` - `varchar(100)`
  - `Address` - `varchar(255)`
  - `City` - `varchar(100)`
  - `Country` - `varchar(100)`

### `room`

- Rows: 40
- Columns:
  - `ID` - `int(11)`
  - `Size` - `int(11)`
  - `Type` - `varchar(50)`
  - `Price` - `decimal(10,2)`
  - `Hotel_ID` - `int(11)`

### `specific_service`

- Rows: 2
- Columns:
  - `ID` - `int(11)`
  - `Type` - `varchar(100)`
  - `Duration` - `int(11)`
  - `Price` - `decimal(10,2)`
  - `Wellness_Center_ID` - `int(11)`

### `stock_market_title`

- Rows: 2
- Columns:
  - `ID` - `int(11)`
  - `Type` - `varchar(100)`

### `wellness_center`

- Rows: 1
- Columns:
  - `ID` - `int(11)`
  - `Name` - `varchar(100)`
  - `Address` - `varchar(255)`
  - `City` - `varchar(100)`
  - `Country` - `varchar(100)`
  - `Resort_ID` - `int(11)`

## `hotel_warehouse`

### `dim_date`

- Rows: 437
- Columns:
  - `DATEID` - `date`
  - `full_date` - `date`
  - `month` - `int(3)`
  - `year` - `int(5)`
  - `season` - `varchar(6)`
  - `is_weekend` - `int(1)`
  - `is_holiday` - `int(1)`
  - `is_event` - `int(1)`

### `dim_person`

- Rows: 200
- Columns:
  - `PersonID` - `varchar(50)`
  - `age_group` - `varchar(6)`
  - `profile_type` - `varchar(8)`
  - `city` - `varchar(100)`
  - `country` - `varchar(100)`
  - `continent_region` - `varchar(11)`

### `dim_room`

- Rows: 40
- Columns:
  - `RoomID` - `int(11)`
  - `room_type` - `varchar(50)`
  - `room_size` - `int(11)`
  - `hotel_city` - `varchar(100)`
  - `hotel_country` - `varchar(100)`
  - `hotel_continent` - `varchar(6)`

### `fact_room_rental`

- Rows: 500
- Columns:
  - `RentallD` - `int(11)`
  - `DateID` - `date`
  - `RoomID` - `int(11)`
  - `PersonID` - `varchar(50)`
  - `period_days` - `int(11)`
  - `room_price_amount` - `decimal(10,2)`
  - `revenue_amount` - `decimal(20,2)`

### `my_first_dbt_model`

- Rows: 2
- Columns:
  - `id` - `int(1)`

### `my_second_dbt_model`

- Rows: 1
- Columns:
  - `id` - `int(1)`

