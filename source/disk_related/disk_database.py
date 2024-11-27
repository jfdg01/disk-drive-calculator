import sqlite3


class DiskDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """Create tables for disks and their stats."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS disks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    main_stat_name TEXT,
                    main_stat_value REAL,
                    main_stat_level INTEGER
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sub_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disk_id INTEGER,
                    name TEXT,
                    value REAL,
                    level INTEGER,
                    FOREIGN KEY (disk_id) REFERENCES disks (id) ON DELETE CASCADE
                )
            """)

    def close(self):
        """Close the database connection."""
        self.connection.close()
