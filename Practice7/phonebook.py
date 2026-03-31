import psycopg2
import csv
from config import load_config

# 1. Загрузка из CSV
def insert_from_csv(file_path):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (phone_number) DO NOTHING", row)
                print("CSV data imported!")
    except Exception as e: print(f"Error: {e}")

# 2. Поиск с фильтрами
def query_contacts(filter_name=None):
    config = load_config()
    sql = "SELECT * FROM phonebook WHERE first_name ILIKE %s"
    arg = (f"%{filter_name}%",) if filter_name else ("%",)
    
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, arg)
            rows = cur.fetchall()
            for row in rows: print(row)

# 3. Удаление
def delete_contact(identifier):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
            print(f"Deleted {cur.rowcount} contact(s).")

# Простая консольная панель
if __name__ == '__main__':
    print("--- PhoneBook Menu ---")
    print("1. Import CSV\n2. View All\n3. Delete Contact")
    choice = input("Select action: ")
    
    if choice == '1':
        insert_from_csv('contacts.csv')
    elif choice == '2':
        query_contacts()
    elif choice == '3':
        name = input("Enter name or phone to delete: ")
        delete_contact(name)