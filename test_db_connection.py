from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg2://hamroh_user:hamroh@localhost:5432/hamroh_db"

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    # Создаем сессию
    db = SessionLocal()
    
    # Попытка выполнить запрос, обернув его в text()
    result = db.execute(text("SELECT 1"))
    print("Database connection successful:", result.fetchone())
except Exception as e:
    print("Database connection failed:", e)
finally:
    db.close()
