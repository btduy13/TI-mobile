from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Đường dẫn đến thư mục data của ứng dụng
DATABASE_DIR = os.path.join(os.path.expanduser('~'), '.tapeinventory')
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# Database URL from desktop app
DATABASE_URL = "postgresql://postgres.ctmkkxfheqjdmjahkheu:M4tkh%40u_11@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

# Tạo engine với SSL mode disable cho PostgreSQL
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "disable"
    }
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các models
Base = declarative_base() 