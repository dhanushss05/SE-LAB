"""Music catalog: stores songs and play counts, rates popularity,
picks a random song and saves/loads playlists."""
import json
import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE songs (id INTEGER PRIMARY KEY, title TEXT, artist TEXT, plays INTEGER)")


def add_song(title, artist, plays=0, playlist=None):
    """Insert a song into the catalog and append its title to the playlist."""
    if playlist is None:
        playlist = []
    conn.execute("INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)", (title, artist, plays))
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Return the id of a random song, or None if the catalog is empty."""
    ids = [r[0] for r in conn.execute("SELECT id FROM songs")]
    return secrets.choice(ids) if ids else None


def popularity(title):
    """Rate a song as 'popular', 'niche' or 'unknown'."""
    row = conn.execute("SELECT plays FROM songs WHERE title = ?", (title,)).fetchone()
    if row is None:
        return "unknown"
    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Serialise a playlist to a JSON string."""
    return json.dumps(playlist)


def load_playlist(blob):
    """Load a playlist from a JSON string."""
    return json.loads(blob)


def total_plays():
    """Return the total play count across all songs."""
    try:
        return conn.execute("SELECT SUM(plays) FROM songs").fetchone()[0] or 0
    except sqlite3.Error:
        return 0


def main():
    """Run a short demonstration of the catalog."""
    pl = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, pl)
    blob = save_playlist(pl)
    l = load_playlist(blob)
    if len(l) > 1:
        print("multi-song playlist")
    print(popularity("Aurora"), popularity("Monsoon"), shuffle_pick(), total_plays())


if __name__ == "__main__":
    main()
