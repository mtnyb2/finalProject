import sqlite3
import datetime
import random


def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    exists = cursor.fetchone() is not None
    if exists:
        print(f"Table {table_name} already exists, skipped")
    return exists

def create_worker_table(cursor):
    if not table_exists(cursor, 'Worker'):
        statement = """CREATE TABLE Worker (national_id_number CHARACTER(10) PRIMARY KEY,
                       first_name VARCHAR(255),
                       last_name VARCHAR(255)
                       );"""
        cursor.execute(statement)
        print("Table Worker created")

def create_customer_table(cursor):
    if not table_exists(cursor, 'Customers'):
        statement = """CREATE TABLE Customers (id INTEGER PRIMARY KEY not null,
                        name VARCHAR(255),
                        phone_number CHARACTER(10),
                        email VARCHAR(255),
                        address VARCHAR(255),
                        age SMALLINT
                        );"""
        cursor.execute(statement)
        print("Table Customers created")

def delete_table(table_name, cursor):
    # Adjusted for proper execution with SQL command
    if table_exists(cursor, table_name):
        cursor.execute(f"DROP TABLE {table_name};")  # Caution: Directly formatting SQL commands carries injection risk.
        print(f"{table_name} dropped")


def create_customer_service_table(cursor):
    if not table_exists(cursor, 'CustomerService'):
        statement = """CREATE TABLE CustomerService(
                    id INTEGER PRIMARY KEY,
                    sale_id BIGINT, 
                    customer_id INTEGER,
                    details TEXT, 
                    type TEXT,
                    status CHARACTER(64),
                    last_updated TEXT,
                    created_date TEXT,
                    worker_name TEXT
                    );"""
        cursor.execute(statement)
        print("Table CustomerService created")

def create_online_sellings(cursor):
    if not table_exists(cursor, 'OnlineSelling'):
        statement = """CREATE TABLE OnlineSelling ( id INTEGER PRIMARY KEY,
                        customer_id BIGINT,
                        status VARCHAR(30),
                        sale_timestamp TEXT,
                        FOREIGN KEY (customer_id) REFERENCES "Customers" ("id")
                        );"""
        cursor.execute(statement)
        print("Table OnlineSelling created")

def create_item_to_sale_table(cursor):
    if not table_exists(cursor, 'SaleToItem'):
        statement = """CREATE TABLE SaleToItem (sale_id BIGINT, item_id BIGINT,
                                                FOREIGN KEY (sale_id) REFERENCES "OnlineSelling" ("id"),
                                                FOREIGN KEY (item_id) REFERENCES "MarketingItems" ("id"))"""
        cursor.execute(statement)


def create_Marketingitems(cursor):
    if not table_exists(cursor, 'MarketingItems'):
        statement = """CREATE TABLE MarketingItems (id INTEGER PRIMARY KEY,
                        manufacturer_name VARCHAR(255),
                        model VARCHAR(255),
                        case_type CHARACTER(15),
                        processor VARCHAR(255),
                        RAM VARCHAR(255),
                        optical_drive VARCHAR(255),
                        OS VARCHAR(255),
                        price INTEGER
                        );"""
        cursor.execute(statement)
        print("Table MarketingItems created")


def insert_customers(cursor):
    statement = """INSERT INTO 'Customers' (name, phone_number,  email, address, age) VALUES (?, ?, ?, ?, ?)"""
    customers = [("Major Corp", "+15463555", "pruchashing@Major.com", "1st street, CO", 19),
                 ("Minor Corp", "+154635551", "pruchashing@Minor.com", "2st street, CO", 19),
                 ("אביב דהן", "+0506648995", "Aviv@gmail.com", "ורד 19 חיפה", 19),
                 ("מאיה גונן", "+0522005888", "Maya@gmail.com", "ויצמן 53, נס ציונה", 19),
                 ("רויטל שקד", "+0502848540", "revi@gmail.com", "בן גוריון 112, ירושלים", 19),
                 ("מאור אסרף", "+0527702869", "maor@gmail.com", "נחמני 52, תל אביב-יפו", 19),
                 ("מיכאל דוידי", "+0546640554", "miki@gmail.com", "דוד ילין 4, חיפה", 19),
                 ("לירן לוי", "+0545540838", "liranlevi@gmail.com", "עופרה חזה 30, קרית מוצקין", 19)]
    for customer in customers:
        cursor.execute(statement, customer)


def insert_marketing_items(curosr):
    statement = "INSERT INTO 'MarketingItems' (manufacturer_name, model, case_type, processor, RAM, optical_drive, OS, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    items = [("Asus", "ZenBook", "16 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "15 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "13 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "12 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "11 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "1 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "1 ince", "i5", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i5", "4GB", "512GB", "Linux", 1500),
             ("Asus", "ZenBook", "16 ince", "i5", "4GB", "512GB", "Linux", 1500),
             ("Asus", "ZenBook", "16 ince", "i5", "4GB", "512GB", "Linux", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Linux", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500),
             ("Asus", "ZenBook", "16 ince", "i7", "4GB", "512GB", "Windows", 1500)]
    for item in items:
        curosr.execute(statement, item)


def insert_customer_sales(cursor):
    major_corp_customer_id = cursor.execute("SELECT id from 'Customers' where name = 'Major Corp';").fetchone()[0]
    minor_corp_customer_id = cursor.execute("SELECT id from 'Customers' where name = 'Minor Corp';").fetchone()[0]
    
    all_marketing_items_ids = [row[0] for row in cursor.execute("SELECT id from 'MarketingItems';").fetchall()]

    for i in range(0, len(all_marketing_items_ids), 3): 
        try:
            item_ids = all_marketing_items_ids[i:i+3]
        except:
            continue
            
        sale_insert = """INSERT INTO 'OnlineSelling' (customer_id, status, sale_timestamp) VALUES (?, ?, ?) RETURNING id"""
        sale_id = cursor.execute(sale_insert, (major_corp_customer_id, "sent", datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10)))).fetchone()[0]
        
        insert_statement = """INSERT INTO SaleToItem (sale_id, item_id) values (?, ?)"""
        for item_id in item_ids:
            cursor.execute(insert_statement, (sale_id, item_id))

def insert_onlineSelling_data(cursor):
    statement = """INSERT INTO OnlineSelling (id, item_id, customer_id, sending_id, sale_price, sale_timestamp)
        VALUES (11,
                112,
                1122,
                10,
                500,
                DATE('now')), (22,
                        223,
                        2233,
                        20,
                        660,
                        DATE('now')), (33,
                                334,
                                3344,
                                30,
                                789,
                                DATE('now')), (44,
                                        445,
                                        4455,
                                        40,
                                        1000,
                                        DATE('now')), (55,
                                                    556,
                                                    5566,
                                                    50,
                                                    1500,
                                                    DATE('now')), (66,
                                                            667,
                                                            6677,
                                                            60,
                                                            2890,
                                                            DATE('now')), (77,
                                                                    778,
                                                                    7788,
                                                                    70,
                                                                    970,
                                                                    DATE('now')), (88,
                                                                            889,
                                                                            8899,
                                                                            80,
                                                                            360,
                                                                            DATE('now')), (99,
                                                                                        990,
                                                                                        9900,
                                                                                        90,
                                                                                        1050,
                                                                                        DATE('now')), (111,
                                                                                                1112,
                                                                                                111222,
                                                                                                110,
                                                                                                780,
                                                                                                DATE('now')), (222,
                                                                                                        2223,
                                                                                                        222333,
                                                                                                        220,
                                                                                                        13000,
                                                                                                        DATE('now')), (333,
                                                                                                                3334,
                                                                                                                333444,
                                                                                                                330,
                                                                                                                1800,
                                                                                                                DATE('now')), (444,
                                                                                                                            4445,
                                                                                                                            444555,
                                                                                                                            440,
                                                                                                                            2074,
                                                                                                                            DATE('now')), (555,
                                                                                                                                    5556,
                                                                                                                                    555666,
                                                                                                                                    550,
                                                                                                                                    2035,
                                                                                                                                    DATE('now')), (666,
                                                                                                                                            6667,
                                                                                                                                            666777,
                                                                                                                                            660,
                                                                                                                                            3746,
                                                                                                                                            DATE('now')), (777,
                                                                                                                                                    7778,
                                                                                                                                                    777888,
                                                                                                                                                    770,
                                                                                                                                                    3580,
                                                                                                                                                    DATE('now')), (888,
                                                                                                                                                                8889,
                                                                                                                                                                888999,
                                                                                                                                                                880,
                                                                                                                                                                5500,
                                                                                                                                                                DATE('now')), (999,
                                                                                                                                                                        9990,
                                                                                                                                                                        999000,
                                                                                                                                                                        990,
                                                                                                                                                                        20,
                                                                                                                                                                        DATE('now'));"""
    cursor.execute(statement)
    print("Data inserted into OnlineSelling")

def main():
    conn = sqlite3.connect('Manual Database.db') 
    cursor = conn.cursor()
    delete_table("CustomService",cursor)
    delete_table("MarketingItems", cursor)
    delete_table("OnlineSelling", cursor)
    delete_table("Customers", cursor)
    delete_table("CustomerService", cursor)
    create_worker_table(cursor)
    create_customer_table(cursor)
    create_customer_service_table(cursor)
    insert_customers(cursor)
    create_Marketingitems(cursor)
    insert_marketing_items(cursor)
    create_online_sellings(cursor)
    create_item_to_sale_table(cursor)
    insert_customer_sales(cursor)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()