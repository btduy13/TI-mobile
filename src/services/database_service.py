from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database.config import SessionLocal
from ..database.models import DonHang, ChiTietDonHang

class DatabaseError(Exception):
    """Base class for database errors"""
    pass

class DatabaseService:
    def __init__(self):
        try:
            self.db: Session = SessionLocal()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Không thể kết nối database: {str(e)}")

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def get_don_hang(self, don_hang_id: int) -> Optional[DonHang]:
        """Lấy thông tin đơn hàng theo ID"""
        try:
            return self.db.query(DonHang).filter(DonHang.id == don_hang_id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Lỗi khi lấy thông tin đơn hàng: {str(e)}")

    def get_all_don_hang(self) -> List[DonHang]:
        """Lấy danh sách tất cả đơn hàng"""
        try:
            return self.db.query(DonHang).order_by(DonHang.ngay_dat.desc()).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Lỗi khi lấy danh sách đơn hàng: {str(e)}")

    def create_don_hang(self, ngay_du_kien: datetime, trang_thai: str, ghi_chu: str = None) -> DonHang:
        """Tạo đơn hàng mới"""
        try:
            don_hang = DonHang(
                ngay_du_kien=ngay_du_kien,
                trang_thai=trang_thai,
                ghi_chu=ghi_chu
            )
            self.db.add(don_hang)
            self.db.commit()
            self.db.refresh(don_hang)
            return don_hang
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Lỗi khi tạo đơn hàng: {str(e)}")

    def update_don_hang(self, don_hang_id: int, **kwargs) -> Optional[DonHang]:
        """Cập nhật thông tin đơn hàng"""
        try:
            don_hang = self.get_don_hang(don_hang_id)
            if don_hang:
                for key, value in kwargs.items():
                    setattr(don_hang, key, value)
                self.db.commit()
                self.db.refresh(don_hang)
            return don_hang
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Lỗi khi cập nhật đơn hàng: {str(e)}")

    def delete_don_hang(self, don_hang_id: int) -> bool:
        """Xóa đơn hàng"""
        try:
            don_hang = self.get_don_hang(don_hang_id)
            if don_hang:
                self.db.delete(don_hang)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Lỗi khi xóa đơn hàng: {str(e)}")

    def add_chi_tiet_don_hang(self, don_hang_id: int, ten_hang: str, 
                             so_luong: int, don_gia: float, quy_cach: str,
                             mau_sac: str, mau_keo: str) -> Optional[ChiTietDonHang]:
        """Thêm chi tiết cho đơn hàng"""
        try:
            don_hang = self.get_don_hang(don_hang_id)
            if don_hang:
                chi_tiet = ChiTietDonHang(
                    don_hang_id=don_hang_id,
                    ten_hang=ten_hang,
                    so_luong=so_luong,
                    don_gia=don_gia,
                    quy_cach=quy_cach,
                    mau_sac=mau_sac,
                    mau_keo=mau_keo
                )
                chi_tiet.calculate_total()
                self.db.add(chi_tiet)
                self.db.commit()
                self.db.refresh(chi_tiet)
                return chi_tiet
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Lỗi khi thêm chi tiết đơn hàng: {str(e)}")

    def get_chi_tiet_don_hang(self, chi_tiet_id: int) -> Optional[ChiTietDonHang]:
        """Lấy thông tin chi tiết đơn hàng theo ID"""
        try:
            return self.db.query(ChiTietDonHang).filter(ChiTietDonHang.id == chi_tiet_id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Lỗi khi lấy thông tin chi tiết đơn hàng: {str(e)}")

    def update_chi_tiet_don_hang(self, chi_tiet_id: int, **kwargs) -> Optional[ChiTietDonHang]:
        """Cập nhật thông tin chi tiết đơn hàng"""
        try:
            chi_tiet = self.get_chi_tiet_don_hang(chi_tiet_id)
            if chi_tiet:
                for key, value in kwargs.items():
                    setattr(chi_tiet, key, value)
                chi_tiet.calculate_total()
                self.db.commit()
                self.db.refresh(chi_tiet)
            return chi_tiet
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Lỗi khi cập nhật chi tiết đơn hàng: {str(e)}") 