import csv
import json
from connect import connect


def print_rows(rows):
    if not rows:
        print("No data found.")
        return

    for row in rows:
        print(row)


def get_or_create_group(cur, group_name):
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        name = input("Name: ").strip()
        email = input("Email: ").strip()
        birthday = input("Birthday (YYYY-MM-DD): ").strip()
        group_name = input("Group (Family/Work/Friend/Other): ").strip()
        phone = input("Phone: ").strip()
        phone_type = input("Phone type (home/work/mobile): ").strip()

        group_id = get_or_create_group(cur, group_name)

        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, email or None, birthday or None, group_id)
        )
        contact_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, phone, phone_type)
        )

        conn.commit()
        print("Contact added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def filter_by_group():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        group_name = input("Enter group name: ").strip()

        cur.execute(
            """
            SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name = %s
            ORDER BY c.name, p.phone
            """,
            (group_name,)
        )

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def search_by_email():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        query = input("Enter email pattern: ").strip()

        cur.execute(
            """
            SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            ORDER BY c.name, p.phone
            """,
            ('%' + query + '%',)
        )

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def show_sorted_contacts():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        print("1 - Sort by name")
        print("2 - Sort by birthday")
        print("3 - Sort by date added")
        choice = input("Choose: ").strip()

        sort_column = "c.name"
        if choice == "2":
            sort_column = "c.birthday"
        elif choice == "3":
            sort_column = "c.created_at"

        query = f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY {sort_column}, c.name
        """
        cur.execute(query)

        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def paginated_navigation():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        limit_value = int(input("Enter page size: ").strip())
        offset_value = 0

        while True:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit_value, offset_value)
            )
            rows = cur.fetchall()

            print("\n--- PAGE ---")
            print_rows(rows)

            cmd = input("Enter next / prev / quit: ").strip().lower()

            if cmd == "next":
                offset_value += limit_value
            elif cmd == "prev":
                offset_value = max(0, offset_value - limit_value)
            elif cmd == "quit":
                break
            else:
                print("Invalid command.")

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def export_to_json(filename="contacts.json"):
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.name
            """
        )
        contacts = cur.fetchall()

        result = []

        for contact in contacts:
            contact_id, name, email, birthday, group_name = contact

            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                (contact_id,)
            )
            phones = cur.fetchall()

            result.append({
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": [{"phone": p[0], "type": p[1]} for p in phones]
            })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print("Exported to JSON successfully.")

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def import_from_json(filename="contacts.json"):
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            name = item["name"]
            email = item.get("email")
            birthday = item.get("birthday")
            group_name = item.get("group", "Other")
            phones_list = item.get("phones", [])

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()

            group_id = get_or_create_group(cur, group_name)

            if existing:
                action = input(f"Contact '{name}' exists. Type skip or overwrite: ").strip().lower()

                if action == "skip":
                    continue
                elif action == "overwrite":
                    contact_id = existing[0]
                    cur.execute(
                        """
                        UPDATE contacts
                        SET email = %s, birthday = %s, group_id = %s
                        WHERE id = %s
                        """,
                        (email, birthday, group_id, contact_id)
                    )
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                else:
                    print("Invalid action. Skipped.")
                    continue
            else:
                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

            for phone_item in phones_list:
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    """,
                    (contact_id, phone_item["phone"], phone_item["type"])
                )

        conn.commit()
        print("Imported from JSON successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def import_from_csv(filename="contacts.csv"):
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                email = row["email"].strip()
                birthday = row["birthday"].strip()
                group_name = row["group"].strip()
                phone = row["phone"].strip()
                phone_type = row["phone_type"].strip()

                group_id = get_or_create_group(cur, group_name)

                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                contact_row = cur.fetchone()

                if contact_row is None:
                    cur.execute(
                        """
                        INSERT INTO contacts(name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (name, email or None, birthday or None, group_id)
                    )
                    contact_id = cur.fetchone()[0]
                else:
                    contact_id = contact_row[0]

                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    """,
                    (contact_id, phone, phone_type)
                )

        conn.commit()
        print("Contacts imported from CSV successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def add_phone_procedure():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        name = input("Contact name: ").strip()
        phone = input("Phone: ").strip()
        phone_type = input("Type (home/work/mobile): ").strip()

        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def move_to_group_procedure():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        name = input("Contact name: ").strip()
        group_name = input("New group: ").strip()

        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        conn.close()


def search_contacts_function():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        query = input("Search query: ").strip()

        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        print_rows(cur.fetchall())

    except Exception as error:
        print("Error:", error)
    finally:
        conn.close()


def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Add contact")
        print("2. Filter by group")
        print("3. Search by email")
        print("4. Sort contacts")
        print("5. Paginated navigation")
        print("6. Export to JSON")
        print("7. Import from JSON")
        print("8. Import from CSV")
        print("9. Add phone (procedure)")
        print("10. Move to group (procedure)")
        print("11. Search contacts (function)")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            search_by_email()
        elif choice == "4":
            show_sorted_contacts()
        elif choice == "5":
            paginated_navigation()
        elif choice == "6":
            export_to_json()
        elif choice == "7":
            import_from_json()
        elif choice == "8":
            import_from_csv()
        elif choice == "9":
            add_phone_procedure()
        elif choice == "10":
            move_to_group_procedure()
        elif choice == "11":
            search_contacts_function()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()