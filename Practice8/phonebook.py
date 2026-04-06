from config import load_config
from connect import connect

def call_search():
    pattern = input("Enter search pattern: ").strip()

    config = load_config()
    conn = connect(config)
    
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
    finally:
        conn.close()

def call_pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    config = load_config()
    conn = connect(config)
    
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
    finally:
        conn.close()

def call_upsert():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    config = load_config()
    conn = connect(config)
    
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print("Inserted/Updated successfully")

        cur.close()
    finally:
        conn.close()

def call_delete():
    value = input("Enter name or phone to delete: ").strip()

    config = load_config()
    conn = connect(config)
    
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Deleted successfully")

        cur.close()
    finally:
        conn.close()

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Search contacts (FUNCTION)")
        print("2. Pagination (FUNCTION)")
        print("3. Insert/Update (PROCEDURE)")
        print("4. Delete (PROCEDURE)")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            call_search()
        elif choice == "2":
            call_pagination()
        elif choice == "3":
            call_upsert()
        elif choice == "4":
            call_delete()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()  