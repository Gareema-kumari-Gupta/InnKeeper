import sqlite3

# Predefined User ID and Password
AUTHORIZED_USER = "admin"
AUTHORIZED_PASSWORD = "password123"


# Connect to MySQL database
def connect_db(): return sqlite3.connect("hotel.db")


# User Authentication
def authenticate_user():
    for attempt in range(3):
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        if user_id == AUTHORIZED_USER and password == AUTHORIZED_PASSWORD:
            print("Authentication Successful! Welcome to the Hotel Management System.")
            return True
        else:
            print(f"Authentication Failed! You have {2 - attempt} attempt(s) remaining.")

    print("Too many failed attempts. Exiting the program.")
    return False

# --------------------------------- DASHBOARD ----------------------------

def dashboard():
    db = connect_db()
    cursor = db.cursor()

    # Total Guests
    cursor.execute("SELECT COUNT(*) FROM guest")
    total_guests = cursor.fetchone()[0]

    # Total Bookings
    cursor.execute("SELECT COUNT(*) FROM booking")
    total_bookings = cursor.fetchone()[0]

    # Total Payments
    cursor.execute("SELECT COUNT(*) FROM payment")
    total_payments = cursor.fetchone()[0]

    print("\n--- Dashboard ---")
    print(f"Total Guests: {total_guests}")
    print(f"Total Bookings: {total_bookings}")
    print(f"Total Payments: {total_payments}")

    cursor.close()
    db.close()

# ---------------- GUEST MANAGEMENT ----------------

def guest_management():
    while True:
        print("\n--- Guest Management ---")
        print("1. Add Guest")
        print("2. Update Guest")
        print("3. Search Guest")
        print("4. Delete Guest")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_guest()
        elif choice == '2':
            update_guest()
        elif choice == '3':
            search_guest()
        elif choice == '4':
            delete_guest()
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")


def add_guest():
    db = connect_db()
    cursor = db.cursor()

    while True:
        custID = input("Enter Customer ID: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        while True:
            try:
                age = int(input("Enter Age: "))
                if age > 0 and age < 120:
                    break
                else:
                    print("Please enter a valid age (1-120).")
            except ValueError:
                print("Invalid input. Please enter a number.")
        sex = input("Enter Sex (M/F): ")
        address = input("Enter Address: ")
        city = input("Enter City: ")
        while True:
            phone_no = input("Enter Phone Number: ")
            if phone_no.isdigit() and len(phone_no) == 10:
                break
            else:
                print("Please enter a valid 10-digit phone number.")
        email = input("Enter Email: ")

        query = """
        INSERT INTO guest (custID, first_name, last_name, age, sex, address, city, phone_no, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = (custID, first_name, last_name, age, sex, address, city, phone_no, email)

        cursor.execute(query, data)
        db.commit()

        print("Guest record added successfully!")

        add_more = input("Do you want to add another guest? (yes/no): ").strip().lower()
        if add_more != "yes":
            break

    cursor.close()
    db.close()


def update_guest():
    db = connect_db()
    cursor = db.cursor()

    custID = input("Enter Customer ID to update: ")

    query_check = "SELECT * FROM guest WHERE custID = ?"
    cursor.execute(query_check, (custID,))
    guest = cursor.fetchone()

    if not guest:
        print("No guest found with the provided Customer ID.")
    else:
        print("\nGuest Found:", guest)
        print("Which field do you want to update?")
        print("1. First Name")
        print("2. Last Name")
        print("3. Age")
        print("4. Sex")
        print("5. Address")
        print("6. City")
        print("7. Phone Number")
        print("8. Email")

        choice = input("Enter your choice (1-8): ")

        field_map = {
            '1': "first_name",
            '2': "last_name",
            '3': "age",
            '4': "sex",
            '5': "address",
            '6': "city",
            '7': "phone_no",
            '8': "email"
        }

        if choice in field_map:
            field_name = field_map[choice]
            new_value = input(f"Enter the new value for {field_name}: ")

            query_update = f"UPDATE guest SET {field_name} = ? WHERE custID = ?"
            cursor.execute(query_update, (new_value, custID))
            db.commit()

            print(f"Guest {field_name} updated successfully!")
        else:
            print("Invalid choice. No changes were made.")

    cursor.close()
    db.close()


def search_guest():
    db = connect_db()
    cursor = db.cursor()

    custID = input("Enter Customer ID to search: ")

    query = "SELECT * FROM guest WHERE custID = ?"
    cursor.execute(query, (custID,))
    result = cursor.fetchone()

    if result:
        print("Guest Found:", result)
    else:
        print("No record found.")

    cursor.close()
    db.close()


def delete_guest():
    db = connect_db()
    cursor = db.cursor()

    custID = input("Enter Customer ID to delete: ")

    query_check = "SELECT * FROM guest WHERE custID = ?"
    cursor.execute(query_check, (custID,))
    guest = cursor.fetchone()

    if not guest:
        print("No guest found with the provided Customer ID.")
    else:
        confirmation = input("Are you sure you want to delete this guest? (yes/no): ").strip().lower()

        if confirmation == "yes":
            query_delete = "DELETE FROM guest WHERE custID = ?"
            cursor.execute(query_delete, (custID,))
            db.commit()
            print("Guest record deleted successfully!")
        else:
            print("Deletion cancelled.")

    cursor.close()
    db.close()


# ---------------- BOOKING MANAGEMENT ----------------

def booking_management():
    while True:
        print("\n--- Booking Management ---")
        print("1. Add Booking")
        print("2. Update Booking")
        print("3. Search Booking")
        print("4. Delete Booking")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_booking()
        elif choice == '2':
            update_booking()
        elif choice == '3':
            search_booking()
        elif choice == '4':
            delete_booking()
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")


def add_booking():
    db = connect_db()
    cursor = db.cursor()

    bookingID = input("Enter Booking ID: ")
    custID = input("Enter Customer ID: ")
    room_no = int(input("Enter Room Number: "))
    type_room = input("Enter Room Type: ")
    checkindate = input("Enter Check-in Date (YYYY-MM-DD): ")
    checkoutdate = input("Enter Check-out Date (YYYY-MM-DD): ")
    noofguest = int(input("Enter Number of Guests: "))
    amtpernight = float(input("Enter Amount per Night: "))
    totalamt = float(input("Enter Total Amount: "))

    query = """
    INSERT INTO booking (bookingID, custID, room_no, type, checkindate, checkoutdate, noofguest, amtpernight, totalamt)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    data = (bookingID, custID, room_no, type_room, checkindate, checkoutdate, noofguest, amtpernight, totalamt)

    cursor.execute(query, data)
    db.commit()

    print("Booking record added successfully!")

    cursor.close()
    db.close()


def update_booking():
    db = connect_db()
    cursor = db.cursor()

    bookingID = input("Enter Booking ID to update: ")

    query_check = "SELECT * FROM booking WHERE bookingID = ?"
    cursor.execute(query_check, (bookingID,))
    booking = cursor.fetchone()

    if not booking:
        print("No booking found with the provided Booking ID.")
    else:
        print("\nBooking Found:", booking)
        print("Which field do you want to update?")
        print("1. Room Number")
        print("2. Check-in Date")
        print("3. Check-out Date")
        print("4. Number of Guests")
        print("5. Amount per Night")

        choice = input("Enter your choice (1-5): ")

        field_map = {
            '1': "room_no",
            '2': "checkindate",
            '3': "checkoutdate",
            '4': "noofguest",
            '5': "amtpernight"
        }

        if choice in field_map:
            field_name = field_map[choice]
            new_value = input(f"Enter the new value for {field_name}: ")

            query_update = f"UPDATE booking SET {field_name} = ? WHERE bookingID = ?"
            cursor.execute(query_update, (new_value, bookingID))
            db.commit()

            print(f"Booking {field_name} updated successfully!")
        else:
            print("Invalid choice. No changes were made.")

    cursor.close()
    db.close()


def search_booking():
    db = connect_db()
    cursor = db.cursor()

    bookingID = input("Enter Booking ID to search: ")

    query = "SELECT * FROM booking WHERE bookingID = ?"
    cursor.execute(query, (bookingID,))
    result = cursor.fetchone()

    if result:
        print("Booking Found:", result)
    else:
        print("No record found.")

    cursor.close()
    db.close()


def delete_booking():
    db = connect_db()
    cursor = db.cursor()

    bookingID = input("Enter Booking ID to delete: ")

    query_check = "SELECT * FROM booking WHERE bookingID = ?"
    cursor.execute(query_check, (bookingID,))
    booking = cursor.fetchone()

    if not booking:
        print("No booking found with the provided Booking ID.")
    else:
        confirmation = input("Are you sure you want to delete this booking? (yes/no): ").strip().lower()

        if confirmation == "yes":
            query_delete = "DELETE FROM booking WHERE bookingID = ?"
            cursor.execute(query_delete, (bookingID,))
            db.commit()
            print("Booking record deleted successfully!")
        else:
            print("Deletion cancelled.")

    cursor.close()
    db.close()


# ---------------- PAYMENT MANAGEMENT ----------------

def payment_management():
    while True:
        print("\n--- Payment Management ---")
        print("1. Add Payment")
        print("2. Update Payment")
        print("3. Search Payment")
        print("4. Delete Payment")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_payment()
        elif choice == '2':
            update_payment()
        elif choice == '3':
            search_payment()
        elif choice == '4':
            delete_payment()
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")


def add_payment():
    db = connect_db()
    cursor = db.cursor()

    bill_no = input("Enter Bill Number: ")
    bookingID = input("Enter Booking ID: ")
    adv_amt = float(input("Enter Advance Amount: "))
    total_amt = float(input("Enter Total Amount: "))
    paymentmethod = input("Enter Payment Method (Cash/Card/Online): ")

    query = """
    INSERT INTO payment (bill_no, bookingID, adv_amt, total_amt, paymentmethod)
    VALUES (?, ?, ?, ?, ?)
    """
    data = (bill_no, bookingID, adv_amt, total_amt, paymentmethod)

    cursor.execute(query, data)
    db.commit()

    print("Payment record added successfully!")

    cursor.close()
    db.close()


def update_payment():
    db = connect_db()
    cursor = db.cursor()

    bill_no = input("Enter Bill Number to update: ")

    query_check = "SELECT * FROM payment WHERE bill_no = ?"
    cursor.execute(query_check, (bill_no,))
    payment = cursor.fetchone()

    if not payment:
        print("No payment record found with the provided Bill Number.")
    else:
        print("\nPayment Found:", payment)
        print("Which field do you want to update?")
        print("1. Advance Amount")
        print("2. Total Amount")
        print("3. Payment Method")

        choice = input("Enter your choice (1-3): ")

        field_map = {
            '1': "adv_amt",
            '2': "total_amt",
            '3': "paymentmethod"
        }

        if choice in field_map:
            field_name = field_map[choice]
            new_value = input(f"Enter the new value for {field_name}: ")

            query_update = f"UPDATE payment SET {field_name} = ? WHERE bill_no = ?"
            cursor.execute(query_update, (new_value, bill_no))
            db.commit()

            print(f"Payment {field_name} updated successfully!")
        else:
            print("Invalid choice. No changes were made.")

    cursor.close()
    db.close()


def search_payment():
    db = connect_db()
    cursor = db.cursor()

    bill_no = input("Enter Bill Number to search: ")

    query = "SELECT * FROM payment WHERE bill_no = ?"
    cursor.execute(query, (bill_no,))
    result = cursor.fetchone()

    if result:
        print("Payment Found:", result)
    else:
        print("No payment record found.")

    cursor.close()
    db.close()


def delete_payment():
    db = connect_db()
    cursor = db.cursor()

    bill_no = input("Enter Bill Number to delete: ")

    query_check = "SELECT * FROM payment WHERE bill_no = ?"
    cursor.execute(query_check, (bill_no,))
    payment = cursor.fetchone()

    if not payment:
        print("No payment record found with the provided Bill Number.")
    else:
        confirmation = input("Are you sure you want to delete this payment record? (yes/no): ").strip().lower()

        if confirmation == "yes":
            query_delete = "DELETE FROM payment WHERE bill_no = ?"
            cursor.execute(query_delete, (bill_no,))
            db.commit()
            print("Payment record deleted successfully!")
        else:
            print("Deletion cancelled.")

    cursor.close()
    db.close()


# ---------------- MAIN MENU ----------------

def main_menu():
    while True:
        print("\n--- Hotel Management System ---")
        print("1. Guest Management")
        print("2. Booking Management")
        print("3. Payment Management")
        print("4. Dashboard")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            guest_management()
        elif choice == '2':
            booking_management()
        elif choice == '3':
            payment_management()
        elif choice == '4':
            dashboard()
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":
    if authenticate_user():
        main_menu()