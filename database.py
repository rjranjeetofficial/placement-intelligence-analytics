import os
import pandas as pd
from sqlalchemy import create_engine, text, URL

# 1. Database Connection Settings
DB_USER = "root"
DB_PASS = "Ranjeet@123"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "campus_db"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "indian_engineering_placement_dataset.csv")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(connection_url)

def init_db():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return

    print("Loading raw CSV data...")
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()

    # Find college and company columns dynamically (case-insensitive)
    cols_lower = {col.lower(): col for col in df.columns}
    
    college_col = cols_lower.get('college_name') or cols_lower.get('college') or cols_lower.get('institution')
    company_col = cols_lower.get('company_name') or cols_lower.get('company')

    with engine.begin() as conn:
        # Load raw dataset into 'students' table
        df.to_sql("students", con=conn, if_exists="replace", index=False)
        print("Table 'students' imported successfully.")

        # Create Colleges lookup table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS colleges (
                college_id INT AUTO_INCREMENT PRIMARY KEY,
                college_name VARCHAR(255) UNIQUE
            );
        """))

        if college_col:
            conn.execute(text(f"""
                INSERT IGNORE INTO colleges (college_name)
                SELECT DISTINCT `{college_col}` FROM students WHERE `{college_col}` IS NOT NULL;
            """))
            print("Table 'colleges' normalized.")

        # Create Companies lookup table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) UNIQUE
            );
        """))

        if company_col:
            conn.execute(text(f"""
                INSERT IGNORE INTO companies (company_name)
                SELECT DISTINCT `{company_col}` FROM students WHERE `{company_col}` IS NOT NULL;
            """))
            print("Table 'companies' normalized.")

        # Create Placements relational table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS placements (
                placement_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                college_id INT,
                company_id INT,
                package_lpa DECIMAL(10,2),
                placement_status VARCHAR(50),
                FOREIGN KEY (college_id) REFERENCES colleges(college_id),
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            );
        """))

    print("\nDatabase initialization and normalization complete!")

def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

if __name__ == "__main__":
    init_db()