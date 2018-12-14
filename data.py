import sqlite3

c = conn.cursor()

def database_init():
    conn = sqlite3.connect('hopper.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS networks(
            ssid text,bssid text,
            latitude  real,
            longitude real,
            signal_strength real)
        CREATE UNIQUE INDEX networks_idx ON networks(id, ssid);
        ''')
    c.commit()
    c.close()

def insert_or_update(data):
    conn = sqlite3.connect('hopper.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO networks()
    ''')
