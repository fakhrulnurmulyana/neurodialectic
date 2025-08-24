from datetime import datetime
import sqlite3

class GameHistory:
    def __init__(self, db_path = "history.db"):
        """Initialize with database path"""
        self.db_path = db_path

    def _connect(self ):
        """Create a connection to the database"""
        return sqlite3.connect(self.db_path)
    
    def create(self, tab_name:str = "history_001", col_name:list=["speaker_code TEXT", "message TEXT", "timestamp TEXT"]):
        """
        Create the history table with additional columns.
        col_names: list of strings, e.g., ["speaker_code TEXT", "message TEXT", "timestamp TEXT"]
        """
        with self._connect() as conn :
            cursor = conn.cursor()

            extra_cols = ", ".join(col_name) if col_name else ""
            
            sql = f"""
                CREATE TABLE IF NOT EXISTS {tab_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                    {', ' if extra_cols else ''}{extra_cols}
                )
            """
            cursor.execute(sql)
            conn.commit()

    def add(self, speaker_code, message, tab_name:str = "history_001"):
        """Add a new record to the history table"""
        with self._connect() as conn :
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql = f"""
                INSERT INTO {tab_name} (speaker_code, message, timestamp)
                VALUES ({speaker_code}, {message}, {timestamp})
            """
            cursor.execute(sql)
            conn.commit()
    
    def get(self, limit:int=5, tab_name:str = "history_001"):
        """Retrieve the latest history records"""
        with self._connect() as conn:
            cursor = conn.cursor()

            sql = f"""
                SELECT speaker_code, message, timestamp
                FROM {tab_name}
                ORDER BY id DESC
                LIMIT {limit}
            """
            cursor.execute(sql)
            return cursor.fetchall()
    
    def get_oph(self, speaker_code, limit:int=5, tab_name:str = "history_001"):
        """Retrieve the latest history records from a single speaker"""
        with self._connect() as conn:
            cursor = conn.cursor()

            sql = f"""
                SELECT speaker_code, message, timestamp
                FROM {tab_name}
                WHERE speaker_code = '{speaker_code}'
                ORDER BY id DESC
                LIMIT {limit}
            """
            cursor.execute(sql)
            return cursor.fetchall()