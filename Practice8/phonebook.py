import psycopg2
from connect import connect
from config import load_config

def main():
    config = load_config()
    conn = connect(config)
    
    if not conn:
        return

    try:
        cur = conn.cursor()

        # Тест 1: Upsert (Добавление/Обновление)
        print("Executing Upsert...")
        cur.execute("CALL upsert_contact(%s, %s);", ('Ivan Ivanov', '87771112233'))
        
        # Тест 2: Массовая вставка
        print("Executing Bulk Insert...")
        names = ['Anna', 'Petr', 'WrongUser']
        phones = ['87012223344', '87023334455', '123'] # '123' вызовет RAISE NOTICE в базе
        cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
        
        # Тест 3: Поиск по шаблону
        print("\nSearching for 'Ivan':")
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", ('Ivan',))
        for row in cur.fetchall():
            print(f"Result: {row}")

        # Тест 4: Пагинация
        print("\nPagination (Limit 2, Offset 0):")
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (2, 0))
        for row in cur.fetchall():
            print(f"Row: {row}")

        # Тест 5: Удаление
        print("\nDeleting contact...")
        cur.execute("CALL delete_contact(%s);", ('Petr',))

        conn.commit()
        print("\nAll tasks completed successfully.")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()