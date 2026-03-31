import csv
from config import load_config
from connect import connect


def create_table():
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE
            )
        """)
        conn.commit()
        print("Table created successfully.")
        cur.close()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def insert_from_console():
    first_name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (first_name, phone)
        )
        conn.commit()
        print("Contact inserted successfully.")
        cur.close()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def insert_from_csv(filename="contacts.csv"):
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                first_name, phone = row
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (first_name, phone)
                )

        conn.commit()
        print("Contacts inserted from CSV successfully.")
        cur.close()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def update_contact():
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()

        search_name = input("Enter the name of contact to update: ").strip()
        print("1 - Update name")
        print("2 - Update phone")
        choice = input("Choose: ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            cur.execute(
                "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
                (new_name, search_name)
            )
        elif choice == "2":
            new_phone = input("Enter new phone: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE first_name = %s",
                (new_phone, search_name)
            )
        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()
        print(f"Updated {cur.rowcount} row(s).")
        cur.close()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def query_contacts():
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()

        print("1 - Show all contacts")
        print("2 - Search by name")
        print("3 - Search by phone prefix")
        choice = input("Choose: ").strip()

        if choice == "1":
            cur.execute("SELECT * FROM phonebook ORDER BY id")
        elif choice == "2":
            name = input("Enter name: ").strip()
            cur.execute(
                "SELECT * FROM phonebook WHERE first_name ILIKE %s ORDER BY id",
                ('%' + name + '%',)
            )
        elif choice == "3":
            prefix = input("Enter phone prefix: ").strip()
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id",
                (prefix + '%',)
            )
        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

        cur.close()
    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def delete_contact():
    config = load_config()
    conn = connect(config)
    if conn is None:
        return

    try:
        cur = conn.cursor()

        print("1 - Delete by name")
        print("2 - Delete by phone")
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ").strip()
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()
        print(f"Deleted {cur.rowcount} row(s).")
        cur.close()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact from console")
        print("3. Insert contacts from CSV")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()