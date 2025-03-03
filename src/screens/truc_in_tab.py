from kivy.lang import Builder
from .base_input_tab import BaseInputTab
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
from ..database.models import TrucInOrder
from ..database.config import SessionLocal

Builder.load_string('''
<TrucInTab>:
    name: "truc_in"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)
        
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
                
                # Thông tin cơ bản
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Thông tin cơ bản"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: ten_hang
                        hint_text: "Tên hàng"
                        helper_text_mode: "on_error"
                        required: True
                        
                    MDTextField:
                        id: ten_khach_hang
                        hint_text: "Tên khách hàng"
                        helper_text_mode: "on_error"
                        required: True
                        
                    MDTextField:
                        id: ngay_du_kien
                        hint_text: "Ngày dự kiến"
                        helper_text_mode: "on_error"
                        required: True
                        readonly: True
                        on_focus: if self.focus: root.show_date_picker(self)
                
                # Thông tin sản phẩm
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Thông tin sản phẩm"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: quy_cach
                        hint_text: "Quy cách"
                        helper_text_mode: "on_error"
                        required: True
                        
                    MDTextField:
                        id: so_luong
                        hint_text: "Số lượng"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: mau_sac
                        hint_text: "Màu sắc"
                        
                    MDTextField:
                        id: mau_keo
                        hint_text: "Màu keo"
                
                # Giá cả
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Giá cả"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: don_gia_goc
                        hint_text: "Đơn giá gốc"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: thanh_tien_goc
                        hint_text: "Thành tiền gốc"
                        readonly: True
                        
                    MDTextField:
                        id: don_gia_ban
                        hint_text: "Đơn giá bán"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: thanh_tien_ban
                        hint_text: "Thành tiền bán"
                        readonly: True
                        
                    MDTextField:
                        id: cong_no_khach
                        hint_text: "Công nợ khách"
                        readonly: True
                
                # CTV và hoa hồng
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "CTV và hoa hồng"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: ctv
                        hint_text: "CTV"
                        
                    MDTextField:
                        id: hoa_hong
                        hint_text: "Hoa hồng (%)"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: tien_hoa_hong
                        hint_text: "Tiền hoa hồng"
                        readonly: True
                        
                    MDTextField:
                        id: loi_nhuan
                        hint_text: "Lợi nhuận"
                        readonly: True
                        
                    MDTextField:
                        id: tien_ship
                        hint_text: "Tiền ship"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: loi_nhuan_rong
                        hint_text: "Lợi nhuận ròng"
                        readonly: True
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(50)
                    padding: [0, dp(10)]
                    
                    Widget:
                        size_hint_x: 0.5
                    
                    MDRaisedButton:
                        text: "Tính toán"
                        on_release: root.tinh_toan()
                        size_hint_x: 0.25
                    
                    MDRaisedButton:
                        text: "Lưu"
                        on_release: root.luu_don_hang()
                        size_hint_x: 0.25
''')

class TrucInTab(BaseInputTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_session = SessionLocal()
        
    def auto_calculate(self, *args):
        """Tự động tính toán khi thay đổi giá trị"""
        self.tinh_toan()
        
    def tinh_toan(self):
        """Tính toán các giá trị"""
        try:
            # Lấy giá trị từ các trường nhập liệu
            so_luong = self.validate_float(self.ids.so_luong.text)
            don_gia_goc = self.validate_float(self.ids.don_gia_goc.text)
            don_gia_ban = self.validate_float(self.ids.don_gia_ban.text)
            hoa_hong = self.validate_float(self.ids.hoa_hong.text)
            tien_ship = self.validate_float(self.ids.tien_ship.text)
            
            if None in [so_luong, don_gia_goc, don_gia_ban]:
                return
                
            # Tính các giá trị
            thanh_tien_goc = don_gia_goc * so_luong
            thanh_tien_ban = don_gia_ban * so_luong
            cong_no_khach = thanh_tien_ban
            loi_nhuan = thanh_tien_ban - thanh_tien_goc
            tien_hoa_hong = loi_nhuan * (hoa_hong or 0) / 100
            loi_nhuan_rong = loi_nhuan - (tien_hoa_hong or 0) - (tien_ship or 0)
            
            # Cập nhật các trường readonly
            self.ids.thanh_tien_goc.text = self.format_currency(thanh_tien_goc)
            self.ids.thanh_tien_ban.text = self.format_currency(thanh_tien_ban)
            self.ids.cong_no_khach.text = self.format_currency(cong_no_khach)
            self.ids.tien_hoa_hong.text = self.format_currency(tien_hoa_hong)
            self.ids.loi_nhuan.text = self.format_currency(loi_nhuan)
            self.ids.loi_nhuan_rong.text = self.format_currency(loi_nhuan_rong)
            
        except Exception as e:
            self.show_error(f"Lỗi khi tính toán: {str(e)}")
            
    def luu_don_hang(self):
        """Lưu đơn hàng vào database"""
        try:
            # Kiểm tra các trường bắt buộc
            required_fields = [
                (self.ids.ten_hang, "Tên hàng"),
                (self.ids.ten_khach_hang, "Tên khách hàng"),
                (self.ids.ngay_du_kien, "Ngày dự kiến"),
                (self.ids.quy_cach, "Quy cách"),
                (self.ids.so_luong, "Số lượng"),
                (self.ids.don_gia_goc, "Đơn giá gốc"),
                (self.ids.don_gia_ban, "Đơn giá bán")
            ]
            
            if not self.validate_required_fields(required_fields):
                return
            
            # Sử dụng session để tạo đơn hàng
            with SessionLocal() as session:
                # Tạo đối tượng đơn hàng (không cần chỉ định ID, model sẽ tự tạo)
                don_hang = TrucInOrder(
                    thoi_gian=datetime.now(),
                    ten_hang=self.ids.ten_hang.text,
                    ten_khach_hang=self.ids.ten_khach_hang.text,
                    ngay_du_kien=datetime.strptime(self.ids.ngay_du_kien.text, "%d/%m/%Y").date(),
                    quy_cach=self.ids.quy_cach.text,
                    so_luong=float(self.ids.so_luong.text),
                    mau_sac=self.ids.mau_sac.text,
                    mau_keo=self.ids.mau_keo.text,
                    don_gia_goc=float(self.ids.don_gia_goc.text),
                    thanh_tien_goc=float(self.ids.thanh_tien_goc.text.replace('đ', '').replace(',', '')),
                    don_gia_ban=float(self.ids.don_gia_ban.text),
                    thanh_tien_ban=float(self.ids.thanh_tien_ban.text.replace('đ', '').replace(',', '')),
                    cong_no_khach=float(self.ids.cong_no_khach.text.replace('đ', '').replace(',', '')),
                    ctv=self.ids.ctv.text,
                    hoa_hong=self.validate_float(self.ids.hoa_hong.text) or 0,
                    tien_hoa_hong=float(self.ids.tien_hoa_hong.text.replace('đ', '').replace(',', '')),
                    loi_nhuan=float(self.ids.loi_nhuan.text.replace('đ', '').replace(',', '')),
                    tien_ship=self.validate_float(self.ids.tien_ship.text) or 0,
                    loi_nhuan_rong=float(self.ids.loi_nhuan_rong.text.replace('đ', '').replace(',', '')),
                    da_giao=False,
                    da_tat_toan=False
                )
                
                # Lưu vào database
                session.add(don_hang)
                session.commit()
                
                # Hiển thị thông báo thành công
                self.show_success(f"Đã lưu đơn hàng {don_hang.id} thành công!")
            
            # Xóa form
            self.xoa_form()
            
        except Exception as e:
            self.show_error(f"Lỗi khi lưu đơn hàng: {str(e)}")
            
    def xoa_form(self):
        """Xóa tất cả các trường trong form"""
        fields_to_clear = [
            self.ids.ten_hang, self.ids.ten_khach_hang, self.ids.ngay_du_kien,
            self.ids.quy_cach, self.ids.so_luong, self.ids.mau_sac,
            self.ids.mau_keo, self.ids.don_gia_goc, self.ids.thanh_tien_goc,
            self.ids.don_gia_ban, self.ids.thanh_tien_ban, self.ids.cong_no_khach,
            self.ids.ctv, self.ids.hoa_hong, self.ids.tien_hoa_hong,
            self.ids.loi_nhuan, self.ids.tien_ship, self.ids.loi_nhuan_rong
        ]
        self.clear_fields(fields_to_clear) 