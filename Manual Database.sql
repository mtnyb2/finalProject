PRAGMA foreign_keys = ON;


CREATE TABLE Worker (id CHARACTER(10) PRIMARY KEY,
                                              name VARCHAR(255),
                                                   fname VARCHAR(255),
                                                         city VARCHAR(255),
                                                              phone_num CHARACTER(10),
                                                                        email VARCHAR(255),
                                                                              gender CHARACTER(6),
                                                                                     department VARCHAR(255),
                                                                                                department_role VARCHAR(255),
                                                                                                                cared_by VARCHAR(255),
                                                                                                                         emergency_contact_name VARCHAR(255),
                                                                                                                                                emergency_contact_phone CHARACTER(10));


CREATE TABLE TinyWorker (id CHARACTER(10) PRIMARY KEY,
                                                  name VARCHAR(255),
                                                       fname VARCHAR(255));


CREATE TABLE RecievedItem (id_recieved_item BIGINT PRIMARY KEY,
                                                           id_shipping BIGINT, makat_id INT, process_by_department VARCHAR(255), item_status VARCHAR(255), item_location VARCHAR(255), recieving_timestamp TIMESTAMP
FOREIGN KEY ("id_recieved_item") REFERENCES "RepairingItems" ("item_id");


FOREIGN KEY ("id_shipping") REFERENCES "Shipping" ("shipping_id");


FOREIGN KEY ("makat_id") REFERENCES "Makat" ("id");

);


CREATE TABLE Sack (id BIGINT PRIMARY KEY,
                                     sale_id BIGINT, item_in_sack INT, weight REAL
FOREIGN KEY ("item_in_sack") REFERENCES "Parts" ("id");


FOREIGN KEY ("sale_id") REFERENCES "RawMaterialSale" ("id");

);


CREATE TABLE Shipping (shipping_id BIGINT PRIMARY KEY,
                                                  supplier_id INT, num_of_pallets SMALLINT, num_of_containers SMALLINT, supplier_comments TEXT, shipping_comments TEXT, driver_id CHARACTER(10), crew_member_id CHARACTER(10), truck_num CHARACTER(8), shipping_date TEXT
FOREIGN KEY ("driver_id") REFERENCES "Worker" ("id");


FOREIGN KEY ("crew_member_id") REFERENCES "Worker" ("id");


FOREIGN KEY ("supplier_id") REFERENCES "Supplier" ("id");

);


CREATE TABLE Supplier (id INT PRIMARY KEY,
                                      name VARCHAR(255),
                                           address VARCHAR(255),
                                                   city VARCHAR(255),
                                                        contact_name VARCHAR(255),
                                                                     phone_num CHARACTER(14),
                                                                               email VARCHAR(255));


CREATE TABLE Buyer (id INT PRIMARY KEY,
                                   name VARCHAR(255),
                                        export_local INT, address VARCHAR(255),
                                                                  type_of_process VARCHAR(255),
                                                                                  contact_name VARCHAR(255),
                                                                                               phone_num CHARACTER(14),
                                                                                                         email VARCHAR(255));


CREATE TABLE parts (id INT PRIMARY KEY,
                                   type VARCHAR(255),
                                        avg_price REAL);


CREATE TABLE RawMaterialSale (id BIGINT PRIMARY KEY,
                                                buyer_id INT, profit_usd REAL, profit_ils REAL, sale_date TEXT
FOREIGN KEY ("buyer_id") REFERENCES "Buyer" ("id");

);


CREATE TABLE Makat (id INT PRIMARY KEY,
                                   category_num REAL category VARCHAR(255),
                                                              subcategory_num REAL subcategory VARCHAR(255),
                                                                                               object_type VARCHAR(255),
                                                                                                           object_avg_weight REAL);


CREATE TABLE RepairingItems (item_id BIGINT PRIMARY KEY,
                                                    makat_id INT, manufacturer_name VARCHAR(255), model VARCHAR(255), case_type CHARACTER(15), processor VARCHAR(255), RAM VARCHAR(255), optical_drive VARCHAR(255), OS VARCHAR(255), id_technician CHARACTER(10), repairing_item_date TEXT
FOREIGN KEY ("id_technician") REFERENCES "Worker" ("id");


FOREIGN KEY ("makat_id") REFERENCES "Makat" ("id");


FOREIGN KEY ("item_id") REFERENCES "MarketingItem" ("item_id");

);


CREATE TABLE MarketingItem ( item_id BIGINT PRIMARY KEY,
                                                    price REAL, date TEXT, picture VARCHAR(255)
FOREIGN KEY ("item_id") REFERENCES "OnlineSelling" ("item_id");

);


CREATE TABLE OnlineSelling (id BIGINT PRIMARY KEY,
                                              item_id BIGINT, costumer_id CHARACTER(10), sending_id VARCHAR(255), sale_price REAL, sale_timestamp TEXT
FOREIGN KEY ("costumer_id") REFERENCES "Customers" ("id");


FOREIGN KEY ("id") REFERENCES "CustomerSercive" ("sale_id");

);


CREATE TABLE Customers (id CHARACTER(10) PRIMARY KEY,
                                                 name VARCHAR(255),
                                                      phone_number CHARACTER(10),
                                                                   email VARCHAR(255),
                                                                         address VARCHAR(255),
                                                                                 age SMALLINT);


CREATE TABLE CustomService ( ticket_id BIGINT sale_id BIGINT, details TEXT, resolved_by TEXT, worker_id CHARACTER(10), timestamp TEXT status CHARACTER(64)
FOREIGN KEY ("worker_id") REFERENCES "Worker" ("id");

);


CREATE TABLE RecievedParts (id BIGINT PRIMARY KEY,
                                              source_id BIGINT, sack_id BIGINT, part_id INT, worker_id CHARACTER(10)
FOREIGN KEY ("worker_id") REFERENCES "Worker" ("id");


FOREIGN KEY ("source_id") REFERENCES "RecievedItem" ("id_recieved_item");


FOREIGN KEY ("sack_id") REFERENCES "Sack" ("id");


FOREIGN KEY ("id") REFERENCES "Parts" ("id");

);