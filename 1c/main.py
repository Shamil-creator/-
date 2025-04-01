import sqlite3

def create_bd():
    connection = sqlite3.connect("my_db.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS rooms(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        )
        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS computers (
        id INTEGER PRIMARY KEY,
        purchase_date DATE NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        room_id INTEGER NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        """)

    connection.commit()
    connection.close()

def data():
    connection = sqlite3.connect("my_db.db")
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO rooms (id, name) VALUES (1, 'Office 101'), (2, 'Office 102')")
    cursor.execute("INSERT INTO computers (id, purchase_date, price, room_id) VALUES (1, '2023-01-15', 1200.50, 1),(2, '2022-07-10', 900.00, 1),(3, '2023-03-05', 1500.75, 2)")
    
    connection.commit()
    connection.close()


def get_computers(room_id):
    conn = sqlite3.connect("my_db.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT c.id, c.purchase_date, c.price, r.name 
    FROM computers c
    JOIN rooms r ON c.room_id = r.id
    WHERE c.room_id = ?
    """, (room_id,))
    
    computers = cursor.fetchall()
    conn.close()
    return computers

def save_to_file(computers, room_name):
    filename = f"computers_in_{room_name.replace(' ', '_')}.txt"
    with open(filename, "w") as f:
        f.write(f"Computers in {room_name}\n")
        f.write("=" * 40 + "\n")
        for comp in computers:
            f.write(f"ID: {comp[0]}, Purchase Date: {comp[1]}, Price: {comp[2]}\n")
    print(f"Data saved to {filename}")


def main():
    # create_bd()
    # data()

    room_id = int(input("Enter room ID: "))
    computers = get_computers(room_id)
    # print(computers)
    
    if computers:
        room_name = computers[0][3]
        save_to_file(computers, room_name)
    else:
        print("No computers found for this room.")

    pass



if __name__ == "__main__":
    main()