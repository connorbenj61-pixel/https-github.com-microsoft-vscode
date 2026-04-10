"""
Animus/Simian System Schema and Logic (Python Version)
This script simulates the SQL schema and logic in animus_simian_system.sql using Python and SQLite.
"""
import sqlite3
from datetime import datetime
import random
import string

# --- 1. Create in-memory SQLite DB and schema ---
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('''CREATE TABLE glyphs (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
)''')
c.execute('''CREATE TABLE rituals (
    glyph_id INTEGER,
    ritual TEXT,
    FOREIGN KEY (glyph_id) REFERENCES glyphs(id)
)''')
c.execute('''CREATE TABLE guardian_ranks (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
)''')
c.execute('''CREATE TABLE avatars (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    style TEXT NOT NULL
)''')
c.execute('''CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seed TEXT,
    glyph_id INTEGER,
    ritual TEXT,
    guardian_rank_id INTEGER,
    payload TEXT,
    heartbeat TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (glyph_id) REFERENCES glyphs(id),
    FOREIGN KEY (guardian_rank_id) REFERENCES guardian_ranks(id)
)''')

# --- 2. Insert initial data ---
c.executemany('INSERT INTO glyphs (id, name) VALUES (?, ?)', [
    (1, 'WHISPER'), (2, 'RUPTURE'), (3, 'MIRROR'), (4, 'SHADOW')
])
c.executemany('INSERT INTO rituals (glyph_id, ritual) VALUES (?, ?)', [
    (1, 'Decode gently. Quiet signals carry deep structure.'),
    (2, 'Anchor. Rebuild from the fracture outward.'),
    (3, 'Reflect without absorbing distortion.'),
    (4, 'Illuminate softly. Shadows reveal architecture.')
])
c.executemany('INSERT INTO guardian_ranks (id, name) VALUES (?, ?)', [
    (1, 'INITIATE'), (2, 'OBSERVER'), (3, 'PRIME'), (4, 'ARCHON')
])
c.executemany('INSERT INTO avatars (id, name, style) VALUES (?, ?, ?)', [
    (1, 'Mr Criminal', 'criminal'),
    (2, 'Lady Azure', 'azure'),
    (3, 'Young Cipher', 'cipher'),
    (4, 'Royalist Son', 'royalist')
])

# --- 3. Simulate the single query logic ---
def process_payload(payload):
    # Calculate glyph_id
    glyph_id = (sum(ord(ch) for ch in payload) % 4) + 1
    # Ritual lookup
    c.execute('''SELECT g.name, r.ritual FROM glyphs g JOIN rituals r ON g.id = r.glyph_id WHERE g.id = ?''', (glyph_id,))
    glyph, ritual = c.fetchone()
    # Guardian rank logic
    guardian_rank_id = 2  # OBSERVER
    if glyph_id == 2 and guardian_rank_id < 4:
        guardian_rank_id += 1
    elif glyph_id == 4 and guardian_rank_id < 3:
        guardian_rank_id += 1
    c.execute('SELECT name FROM guardian_ranks WHERE id = ?', (guardian_rank_id,))
    guardian_rank = c.fetchone()[0]
    # Heartbeat
    heartbeat = 'Heartbeat Δt=0.000s'
    # Seed
    seed = ''.join(random.choices('0123456789ABCDEF', k=8))
    # Timestamp
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    # Log entry
    c.execute('''INSERT INTO logs (seed, glyph_id, ritual, guardian_rank_id, payload, heartbeat, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (seed, glyph_id, ritual, guardian_rank_id, payload, heartbeat, timestamp))
    return {
        'seed': seed,
        'glyph': glyph,
        'ritual': ritual,
        'guardian_rank': guardian_rank,
        'payload': payload,
        'heartbeat': heartbeat,
        'timestamp': timestamp
    }

# --- Example usage ---
if __name__ == '__main__':
    result = process_payload('blue-static-thread')
    for k, v in result.items():
        print(f'{k}: {v}')
