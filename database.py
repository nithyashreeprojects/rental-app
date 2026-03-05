import sqlite3

DATABASE = "rental.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS properties(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   area TEXT NOT NULL,
                   city TEXT NOT NULL,
                   price INTEGER NOT NULL,
                   bedrooms INTEGER NOT NULL,
                   furnishing_type TEXT NOT NULL,
                   has_parking INTEGER DEFAULT 0,
                   has_lift INTEGER DEFAULT 0,
                   is_gated_community INTEGER DEFAULT 0,
                   pets_allowed INTEGER DEFAULT 0,
                   maintenance_included INTEGER DEFAULT 0,
                   available_from TEXT,
                   description TEXT
                   )
        ''')
    conn.commit()
    conn.close()


def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties")
    count = cursor.fetchone()[0]
    if count == 0:
        properties = [
            ("Cozy 1BHK Apartment", "Anna Nagar", "Chennai", 8000, 1, "semi-furnished", 0, 0, 1, 0, 1, "01/06/2026", "A bright cozy apartment perfect for a single occupant or couple."),
            ("Spacious 2BHK", "Adyar", "Chennai", 14000, 2, "furnished", 1, 1, 1, 0, 0, "15/05/2026", "Well ventilated apartment near Adyar beach."),
            ("Budget 1BHK", "T Nagar", "Chennai", 6000, 1, "unfurnished", 0, 0, 0, 0, 0, "01/05/2026", "Affordable room close to shopping areas."),
            ("Family 3BHK", "Velachery", "Chennai", 18000, 3, "semi-furnished", 1, 1, 1, 1, 1, "01/06/2026", "Spacious gated community home perfect for families."),
            ("Quiet 1BHK", "Mylapore", "Chennai", 10000, 1, "furnished", 0, 0, 1, 1, 0, "01/05/2026", "Quiet neighbourhood, very safe area."),
            ("Metro 2BHK", "Arumbakkam", "Chennai", 12000, 2, "semi-furnished", 1, 0, 0, 0, 1, "15/05/2026", "Close to Arumbakkam metro station."),
            ("Secure 2BHK", "Anna Nagar", "Chennai", 15000, 2, "furnished", 1, 1, 1, 0, 1, "01/06/2026", "Premium gated community with 24hr security."),
            ("Budget Studio", "Koyambedu", "Chennai", 5000, 1, "unfurnished", 0, 0, 0, 0, 0, "01/05/2026", "Very affordable, close to Koyambedu bus terminus."),
            ("Premium 3BHK", "Adyar", "Chennai", 28000, 3, "furnished", 1, 1, 1, 1, 1, "15/06/2026", "Luxury apartment in prime Adyar location."),
            ("Cozy 2BHK", "Mogappair", "Chennai", 11000, 2, "semi-furnished", 0, 1, 1, 0, 0, "01/05/2026", "Well maintained apartment in peaceful locality."),
        ]
        cursor.executemany('''
                INSERT INTO properties (title,area,city,price,bedrooms,furnishing_type,has_parking,has_lift,is_gated_community, pets_allowed,maintenance_included,available_from,description)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) ''',properties)
        conn.commit()
    conn.close()


def fetch_properties():
    conn = get_connection()
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()
    conn.close()
    return properties


def init_db():
    create_tables()
    seed_data()


if __name__ == "__main__":
    init_db()
    print("Database created successfully!")