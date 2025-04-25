import psycopg2
import csv

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    port="7050",
    user="postgres",
    password="Tkso0507."
)
cur = conn.cursor()

# 1. Design table
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        );
    """)
    conn.commit()

# 2. Insert data from CSV
def insert_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()

# 2. Insert from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()

# 3. Update data
def update_data():
    field = input("What do you want to update? (name/phone): ")
    current = input(f"Current {field}: ")
    new_value = input(f"New {field}: ")
    cur.execute(f"UPDATE PhoneBook SET {field} = %s WHERE {field} = %s", (new_value, current))
    conn.commit()

# 4. Show all entries
def show_all_entries():
    cur.execute("SELECT name, phone FROM PhoneBook ORDER BY name;")
    rows = cur.fetchall()
    if not rows:
        print("PhoneBook is empty.")
    else:
        print("\nPhoneBook entries:")
        for row in rows:
            print(f"Name: {row[0]}  |  Phone: {row[1]}")

# 5. Query data
def query_data():
    filter_field = input("Filter by name or phone: ")
    filter_value = input(f"Enter {filter_field}: ")
    cur.execute(f"SELECT * FROM PhoneBook WHERE {filter_field} = %s", (filter_value,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def query_data_by_firstletter():
    filter_letter = input("Enter the first letter of the name to filter: ").strip()
    like_pattern = filter_letter + '%'
    cur.execute("SELECT * FROM PhoneBook WHERE name LIKE %s", (like_pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# 6. Delete data
def delete_data():
    field = input("Delete by name or phone: ")
    value = input(f"Enter {field}: ")
    cur.execute(f"DELETE FROM PhoneBook WHERE {field} = %s", (value,))
    conn.commit()

# NEW TASK: Function to return all records by pattern
def search_by_pattern():
    pattern = input("Enter part of name or phone: ")
    cur.execute("SELECT * FROM PhoneBook WHERE name ILIKE %s OR phone ILIKE %s", (f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# NEW TASK: Procedure to insert or update a single user
def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("SELECT * FROM PhoneBook WHERE name = %s", (name,))
    if cur.fetchone():
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE name = %s", (phone, name))
        print("Phone updated.")
    else:
        cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (name, phone))
        print("New user added.")
    conn.commit()

# NEW TASK: Insert multiple users and return invalid ones
def insert_many_users():
    invalid_entries = []
    count = int(input("How many users do you want to insert? "))
    for _ in range(count):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        if not phone.isdigit():
            invalid_entries.append((name, phone))
            continue
        cur.execute("SELECT * FROM PhoneBook WHERE name = %s", (name,))
        if cur.fetchone():
            cur.execute("UPDATE PhoneBook SET phone = %s WHERE name = %s", (phone, name))
        else:
            cur.execute("INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    if invalid_entries:
        print("Invalid entries:")
        for entry in invalid_entries:
            print(f"Name: {entry[0]} | Phone: {entry[1]}")

# NEW TASK: Query with pagination
def query_with_pagination():
    try:
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))
        cur.execute("""
            SELECT id, name, phone FROM PhoneBook 
            ORDER BY id 
            LIMIT %s OFFSET %s
        """, (limit, offset))
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Error occurred during pagination query:", e)

# NEW TASK: Delete by username or phone
def delete_by_name_or_phone():
    field = input("Delete by 'name' or 'phone': ").strip().lower()
    if field not in ['name', 'phone']:
        print("Invalid input. Choose 'name' or 'phone'.")
        return
    value = input(f"Enter {field}: ")
    cur.execute(f"DELETE FROM PhoneBook WHERE {field} = %s", (value,))
    conn.commit()
    print("Record deleted.")

# Menu
def main():
    create_table()
    while True:
        print("\nOptions:")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update data")
        print("4. Show all entries")
        print("5. Query data")
        print("6. Query by first letter")
        print("7. Delete data")
        print("8. Search by pattern")  # NEW
        print("9. Insert or update user")  # NEW
        print("10. Insert many users")  # NEW
        print("11. Query with pagination")  # NEW
        print("12. Delete by name or phone")  # NEW
        print("13. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            insert_from_csv(input("CSV file path: "))
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_data()
        elif choice == '4':
            show_all_entries()
        elif choice == '5':
            query_data()
        elif choice == '6':
            query_data_by_firstletter()
        elif choice == '7':
            delete_data()
        elif choice == '8':
            search_by_pattern()
        elif choice == '9':
            insert_or_update_user()
        elif choice == '10':
            insert_many_users()
        elif choice == '11':
            query_with_pagination()
        elif choice == '12':
            delete_by_name_or_phone()
        elif choice == '13':
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
