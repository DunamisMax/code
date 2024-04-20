import sqlite3
import logging
import config

logger = logging.getLogger(__name__)  # Basic logger setup


def create_connection():
    """Creates a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(config.DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
    return None


def create_tables(conn):
    """Creates the required tables if they don't exist."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS studies (
            study_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            study_date TEXT,
            modality TEXT,
            description TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_id INTEGER,
            file_path TEXT,
            sop_instance_uid TEXT,  -- Store DICOM unique identifier
            FOREIGN KEY (study_id) REFERENCES studies(study_id)
        )
    """
    )
    conn.commit()


def insert_study(conn, study_data):
    """Inserts a new study into the database.

    Args:
        conn: Database connection object
        study_data: Dictionary containing 'patient_name', 'study_date', 'modality', 'description'
    """
    sql = """INSERT INTO studies(patient_name, study_date, modality, description)
             VALUES (?, ?, ?, ?)"""
    cursor = conn.cursor()
    cursor.execute(sql, tuple(study_data.values()))
    conn.commit()
    return cursor.lastrowid  # Return the newly generated study_id


def insert_image(conn, image_data):
    """Inserts a new image record.

    Args:
        conn: Database connection object
        image_data: Dictionary containing 'study_id', 'file_path', 'sop_instance_uid'
    """
    sql = """INSERT INTO images(study_id, file_path, sop_instance_uid) 
             VALUES (?, ?, ?)"""
    cursor = conn.cursor()
    cursor.execute(sql, tuple(image_data.values()))
    conn.commit()
    return cursor.lastrowid


def query_studies(conn):
    """Fetches a list of studies from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM studies")
    return cursor.fetchall()


# ... Add more functions as needed:
#     - query_images_by_study(conn, study_id)
#     - update_study(conn, study_id, new_data)
#     - etc.

if __name__ == "__main__":
    # Initial setup (Do this only once when the database is first created)
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()
