from .config import Base, engine

def init_database():
    """Khởi tạo database và tạo các bảng"""
    Base.metadata.create_all(bind=engine) 