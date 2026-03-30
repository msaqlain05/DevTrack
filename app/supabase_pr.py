import psycopg2
import logging
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()


DATABASE_URL = "postgresql://postgres.aqqyutywiiwzrsmithsf:Dev-pass_123@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            logger.info("✅ Connected to database")
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("🔌 Connection closed")

    def execute(self, query, params=None, fetch=False):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)

                if fetch:
                    result = cursor.fetchall()
                    logger.info(f"📦 Fetched {len(result)} records")
                    return result

                self.conn.commit()
                logger.info("💾 Query executed successfully")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"❌ Query failed: {e}")
            raise


# Initialize DB
db = Database(DATABASE_URL)

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    db.execute(query)
    logger.info("📊 Table 'products' ready")


def insert_product(name, price):
    query = """
    INSERT INTO products (name, price)
    VALUES (%s, %s)
    RETURNING id;
    """
    result = db.execute(query, (name, price), fetch=True)
    logger.info(f"➕ Product inserted with ID: {result[0]['id']}")


def get_products():
    query = "SELECT * FROM products ORDER BY id DESC;"
    products = db.execute(query, fetch=True)

    for p in products:
        logger.info(f"🛒 {p['id']} | {p['name']} | ${p['price']}")

    return products


if __name__ == "__main__":
    try:
        db.connect()

        create_table()

        # Insert sample data
        insert_product("Laptop", 1200.50)
        insert_product("Mouse", 25.99)

        # Retrieve data
        products = get_products()

        print("\nFinal Data:")
        for p in products:
            print(p)

    finally:
        db.close()