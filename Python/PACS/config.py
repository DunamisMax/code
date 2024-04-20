# Database Settings
DATABASE_ENGINE = "sqlite3"  # Choices: 'sqlite3', 'postgresql', 'mysql', etc.
DATABASE_NAME = "dicom_pacs.db"  # Name of your database file (SQLite)

# For PostgreSQL or MySQL:
# DATABASE_USER = 'your_username'
# DATABASE_PASSWORD = 'your_password'
# DATABASE_HOST = 'your_database_host'  # e.g., 'localhost'
# DATABASE_PORT = '5432'  # Adjust for your database server's port

# Advanced/Optional Settings:
DICOM_STORAGE_PATH = "./data/images"  # Where to store incoming DICOMs
LOG_LEVEL = "INFO"  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
