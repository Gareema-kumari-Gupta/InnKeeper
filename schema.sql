PRAGMA foreign_keys = ON;

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS guest;

CREATE TABLE guest (
  custID TEXT PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  age INTEGER DEFAULT NULL,
  sex TEXT DEFAULT NULL,
  address TEXT NOT NULL,
  city TEXT NOT NULL,
  phone_no TEXT NOT NULL,
  email TEXT DEFAULT NULL
);

INSERT INTO guest VALUES 
('G001','John','Doe',28,'M','123 Elm St.','New York','987654321','john.doe@example.com'),
('G002','Jane','Smith',34,'F','456 Oak St.','Los Angeles','987654321','jane.smith@example.com'),
('G003','Alice','Johnson',26,'F','789 Pine St.','Chicago','987654321','alice.johnson@example.com'),
('G004','Robert','Brown',45,'M','101 Maple St.','Houston','987654313','robert.brown@example.com'),
('G005','Mary','Davis',30,'F','202 Cedar St.','Phoenix','987643214','mary.davis@example.com');

CREATE TABLE booking (
  bookingID TEXT PRIMARY KEY,
  custID TEXT DEFAULT NULL,
  room_no INTEGER DEFAULT NULL,
  type TEXT NOT NULL,
  checkindate TEXT NOT NULL,
  checkoutdate TEXT NOT NULL,
  noofguest INTEGER NOT NULL DEFAULT 1,
  amtpernight REAL DEFAULT 500.00,
  totalamt REAL DEFAULT NULL,
  FOREIGN KEY (custID) REFERENCES guest (custID)
);

INSERT INTO booking VALUES 
('B001','G001',101,'Deluxe','2024-11-01','2024-11-05',2,500.00,2000.00),
('B002','G002',102,'Standard','2024-11-03','2024-11-06',1,400.00,1200.00),
('B003','G003',103,'Suite','2024-11-02','2024-11-07',3,800.00,4000.00),
('B004','G004',104,'Single','2024-11-04','2024-11-05',1,300.00,300.00),
('B005','G005',105,'Double','2024-11-01','2024-11-04',2,450.00,1350.00);

CREATE TABLE payment (
  bill_no TEXT PRIMARY KEY,
  bookingID TEXT DEFAULT NULL,
  adv_amt REAL DEFAULT NULL,
  total_amt REAL DEFAULT NULL,
  remaining_amt REAL GENERATED ALWAYS AS (total_amt - adv_amt) VIRTUAL,
  paymentmethod TEXT DEFAULT NULL,
  FOREIGN KEY (bookingID) REFERENCES booking (bookingID)
);

INSERT INTO payment (bill_no, bookingID, adv_amt, total_amt, paymentmethod) VALUES 
('P001','B001',1000.00,2000.00,'Cr Card'),
('P002','B002',500.00,1200.00,'Dr Card'),
('P003','B003',2000.00,4000.00,'Cash'),
('P004','B004',300.00,300.00,'Cr Card'),
('P005','B005',800.00,1350.00,'Cash');