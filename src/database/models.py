from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base, SessionLocal

def generate_order_id(prefix, session):
    """Generate order ID with format: prefix-MM-YY-XXX"""
    today = datetime.now()
    month = today.strftime("%m")  # Format: MM
    year = today.strftime("%y")   # Format: YY
    
    # Get the last order number for this month and year based on prefix
    if prefix == "BKI":
        model = BangKeoInOrder
    elif prefix == "TI":
        model = TrucInOrder
    else:
        model = BangKeoOrder
        
    # Get the last order number for this month and year
    last_order = session.query(func.max(func.substr(model.id, -3))).filter(
        model.id.like(f"{prefix}-{month}-{year}%")
    ).scalar()
    
    if last_order is None:
        next_number = 1
    else:
        next_number = int(last_order) + 1
        
    # Format: PREFIX-MM-YY-XXX (where XXX is a 3-digit number)
    return f"{prefix}-{month}-{year}-{next_number:03d}"

class BangKeoInOrder(Base):
    __tablename__ = 'bang_keo_in_orders'

    PREFIX = "BKI"
    
    id = Column(String(20), primary_key=True)
    thoi_gian = Column(DateTime, default=datetime.now)
    ten_hang = Column(String(255), nullable=False)
    ten_khach_hang = Column(String(255), nullable=False)
    ngay_du_kien = Column(Date, nullable=False)
    
    # Quy cách
    quy_cach_mm = Column(Float)
    quy_cach_m = Column(Float)
    quy_cach_mic = Column(Float)
    cuon_cay = Column(Float)
    
    # Số lượng và phí
    so_luong = Column(Float, nullable=False)
    phi_sl = Column(Float, default=0)
    mau_keo = Column(String(100))
    phi_keo = Column(Float, default=0)
    mau_sac = Column(String(100))
    phi_mau = Column(Float, default=0)
    phi_size = Column(Float, default=0)
    phi_cat = Column(Float, default=0)
    
    # Giá cả
    don_gia_von = Column(Float, default=0)
    don_gia_goc = Column(Float, default=0)
    thanh_tien_goc = Column(Float, default=0)
    don_gia_ban = Column(Float, nullable=False)
    thanh_tien_ban = Column(Float, default=0)
    tien_coc = Column(Float, default=0)
    cong_no_khach = Column(Float, default=0)
    
    # CTV và hoa hồng
    ctv = Column(String(100))
    hoa_hong = Column(Float, default=0)
    tien_hoa_hong = Column(Float, default=0)
    
    # Thông tin thêm
    loi_giay = Column(String(100))
    thung_bao = Column(String(100))
    loi_nhuan = Column(Float, default=0)
    tien_ship = Column(Float, default=0)
    loi_nhuan_rong = Column(Float, default=0)

    # Trạng thái đơn hàng
    da_giao = Column(Boolean, default=False)
    da_tat_toan = Column(Boolean, default=False)

    @classmethod
    def generate_id(cls, session):
        return generate_order_id(cls.PREFIX, session)
        
    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            session = SessionLocal()
            kwargs['id'] = self.generate_id(session)
            session.close()
        super().__init__(**kwargs)

class TrucInOrder(Base):
    __tablename__ = 'truc_in_orders'

    PREFIX = "TI"
    
    id = Column(String(20), primary_key=True)
    thoi_gian = Column(DateTime, default=datetime.now)
    ten_hang = Column(String(255), nullable=False)
    ten_khach_hang = Column(String(255), nullable=False)
    ngay_du_kien = Column(Date, nullable=False)
    
    # Thông tin cơ bản
    quy_cach = Column(String(100))
    so_luong = Column(Float, nullable=False)
    mau_sac = Column(String(100))
    mau_keo = Column(String(100))
    
    # Giá cả
    don_gia_goc = Column(Float, default=0)
    thanh_tien_goc = Column(Float, default=0)
    don_gia_ban = Column(Float, nullable=False)
    thanh_tien_ban = Column(Float, default=0)
    cong_no_khach = Column(Float, default=0)
    
    # CTV và hoa hồng
    ctv = Column(String(100))
    hoa_hong = Column(Float, default=0)
    tien_hoa_hong = Column(Float, default=0)
    loi_nhuan = Column(Float, default=0)
    tien_ship = Column(Float, default=0)
    loi_nhuan_rong = Column(Float, default=0)

    # Trạng thái đơn hàng
    da_giao = Column(Boolean, default=False)
    da_tat_toan = Column(Boolean, default=False)

    @classmethod
    def generate_id(cls, session):
        return generate_order_id(cls.PREFIX, session)
        
    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            session = SessionLocal()
            kwargs['id'] = self.generate_id(session)
            session.close()
        super().__init__(**kwargs)

class BangKeoOrder(Base):
    __tablename__ = 'bang_keo_orders'

    PREFIX = "BK"
    
    id = Column(String(20), primary_key=True)
    thoi_gian = Column(DateTime, default=datetime.now)
    ten_hang = Column(String(255), nullable=False)
    ten_khach_hang = Column(String(255), nullable=False)
    ngay_du_kien = Column(Date, nullable=False)
    
    # Thông tin cơ bản
    quy_cach = Column(String(100))  # In KG
    so_luong = Column(Float, nullable=False)
    mau_sac = Column(String(100))
    
    # Giá cả
    don_gia_goc = Column(Float, default=0)
    thanh_tien = Column(Float, default=0)
    don_gia_ban = Column(Float, nullable=False)
    thanh_tien_ban = Column(Float, default=0)
    cong_no_khach = Column(Float, default=0)
    
    # CTV và hoa hồng
    ctv = Column(String(100))
    hoa_hong = Column(Float, default=0)
    tien_hoa_hong = Column(Float, default=0)
    loi_nhuan = Column(Float, default=0)
    tien_ship = Column(Float, default=0)
    loi_nhuan_rong = Column(Float, default=0)

    # Trạng thái đơn hàng
    da_giao = Column(Boolean, default=False)
    da_tat_toan = Column(Boolean, default=False)

    @classmethod
    def generate_id(cls, session):
        return generate_order_id(cls.PREFIX, session)
        
    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            session = SessionLocal()
            kwargs['id'] = self.generate_id(session)
            session.close()
        super().__init__(**kwargs)

# Giữ lại các model cũ cho tương thích ngược
class DonHang(Base):
    __tablename__ = 'don_hang'

    id = Column(Integer, primary_key=True)
    ngay_dat = Column(DateTime, default=datetime.now)
    ngay_du_kien = Column(DateTime)
    trang_thai = Column(String)
    da_giao = Column(Boolean, default=False)
    da_tat_toan = Column(Boolean, default=False)
    ghi_chu = Column(String)
    
    # Relationship with ChiTietDonHang
    chi_tiet = relationship("ChiTietDonHang", back_populates="don_hang", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DonHang(id={self.id}, ngay_dat='{self.ngay_dat}', trang_thai='{self.trang_thai}')>"

class ChiTietDonHang(Base):
    __tablename__ = 'chi_tiet_don_hang'

    id = Column(Integer, primary_key=True)
    don_hang_id = Column(Integer, ForeignKey('don_hang.id'))
    ten_hang = Column(String)
    so_luong = Column(Integer)
    don_gia = Column(Float)
    thanh_tien = Column(Float)
    quy_cach = Column(String)
    mau_sac = Column(String)
    mau_keo = Column(String)
    
    # Relationship with DonHang
    don_hang = relationship("DonHang", back_populates="chi_tiet")

    def __repr__(self):
        return f"<ChiTietDonHang(id={self.id}, ten_hang='{self.ten_hang}', so_luong={self.so_luong})>"

    def calculate_total(self):
        """Tính tổng tiền cho chi tiết đơn hàng"""
        self.thanh_tien = self.so_luong * self.don_gia 