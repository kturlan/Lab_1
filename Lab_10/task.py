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

# 4. show all entries
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

# Example menu-driven usage
def main():
    create_table()
    while True:
        print("\nOptions:")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update data")
        print("4. show all entries")
        print("5. Query data")
        print("6. Query data by first letter")
        print("7. Delete data")
        print("8. Exit")

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
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()