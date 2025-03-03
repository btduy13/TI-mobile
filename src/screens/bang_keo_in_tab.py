from kivy.lang import Builder
from .base_input_tab import BaseInputTab
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
from ..database.models import BangKeoInOrder
from ..database.config import SessionLocal

Builder.load_string('''
<BangKeoInTab>:
    name: "bang_keo_in"
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
                
                # Quy cách
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Quy cách"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: quy_cach_mm
                        hint_text: "Quy cách (mm)"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        
                    MDTextField:
                        id: quy_cach_m
                        hint_text: "Quy cách (m)"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        
                    MDTextField:
                        id: quy_cach_mic
                        hint_text: "Quy cách (mic)"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        
                    MDTextField:
                        id: cuon_cay
                        hint_text: "Cuộn/Cây"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                
                # Số lượng và phí
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Số lượng và phí"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: so_luong
                        hint_text: "Số lượng"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: phi_sl
                        hint_text: "Phí số lượng"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: mau_keo
                        hint_text: "Màu keo"
                        
                    MDTextField:
                        id: phi_keo
                        hint_text: "Phí keo"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: mau_sac
                        hint_text: "Màu sắc"
                        
                    MDTextField:
                        id: phi_mau
                        hint_text: "Phí màu"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: phi_size
                        hint_text: "Phí size"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: phi_cat
                        hint_text: "Phí cắt"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                
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
                        id: don_gia_von
                        hint_text: "Đơn giá vốn"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        required: True
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: don_gia_goc
                        hint_text: "Đơn giá gốc"
                        readonly: True
                        
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
                        id: tien_coc
                        hint_text: "Tiền cọc"
                        helper_text_mode: "on_error"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
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
                
                # Thông tin thêm
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDLabel:
                        text: "Thông tin thêm"
                        bold: True
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: loi_giay
                        hint_text: "Lõi giấy"
                        
                    MDTextField:
                        id: thung_bao
                        hint_text: "Thùng/Bao"
                        
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

class BangKeoInTab(BaseInputTab):
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
            don_gia_von = self.validate_float(self.ids.don_gia_von.text)
            phi_sl = self.validate_float(self.ids.phi_sl.text)
            phi_keo = self.validate_float(self.ids.phi_keo.text)
            phi_mau = self.validate_float(self.ids.phi_mau.text)
            phi_size = self.validate_float(self.ids.phi_size.text)
            phi_cat = self.validate_float(self.ids.phi_cat.text)
            don_gia_ban = self.validate_float(self.ids.don_gia_ban.text)
            tien_coc = self.validate_float(self.ids.tien_coc.text)
            hoa_hong = self.validate_float(self.ids.hoa_hong.text)
            tien_ship = self.validate_float(self.ids.tien_ship.text)
            
            if None in [so_luong, don_gia_von, don_gia_ban]:
                return
                
            # Tính đơn giá gốc
            don_gia_goc = don_gia_von + phi_sl + phi_keo + phi_mau + phi_size + phi_cat
            
            # Tính các giá trị khác
            thanh_tien_goc = don_gia_goc * so_luong
            thanh_tien_ban = don_gia_ban * so_luong
            cong_no_khach = thanh_tien_ban - (tien_coc or 0)
            loi_nhuan = thanh_tien_ban - thanh_tien_goc
            tien_hoa_hong = loi_nhuan * (hoa_hong or 0) / 100
            loi_nhuan_rong = loi_nhuan - (tien_hoa_hong or 0) - (tien_ship or 0)
            
            # Cập nhật các trường readonly
            self.ids.don_gia_goc.text = self.format_currency(don_gia_goc)
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
                (self.ids.quy_cach_mm, "Quy cách (mm)"),
                (self.ids.quy_cach_m, "Quy cách (m)"),
                (self.ids.quy_cach_mic, "Quy cách (mic)"),
                (self.ids.cuon_cay, "Cuộn/Cây"),
                (self.ids.so_luong, "Số lượng"),
                (self.ids.don_gia_von, "Đơn giá vốn"),
                (self.ids.don_gia_ban, "Đơn giá bán")
            ]
            
            if not self.validate_required_fields(required_fields):
                return
            
            # Sử dụng session để tạo đơn hàng
            with SessionLocal() as session:
                # Tạo đối tượng đơn hàng (không cần chỉ định ID, model sẽ tự tạo)
                don_hang = BangKeoInOrder(
                    thoi_gian=datetime.now(),
                    ten_hang=self.ids.ten_hang.text,
                    ten_khach_hang=self.ids.ten_khach_hang.text,
                    ngay_du_kien=datetime.strptime(self.ids.ngay_du_kien.text, "%d/%m/%Y").date(),
                    quy_cach_mm=float(self.ids.quy_cach_mm.text),
                    quy_cach_m=float(self.ids.quy_cach_m.text),
                    quy_cach_mic=float(self.ids.quy_cach_mic.text),
                    cuon_cay=float(self.ids.cuon_cay.text),
                    so_luong=float(self.ids.so_luong.text),
                    phi_sl=self.validate_float(self.ids.phi_sl.text) or 0,
                    mau_keo=self.ids.mau_keo.text,
                    phi_keo=self.validate_float(self.ids.phi_keo.text) or 0,
                    mau_sac=self.ids.mau_sac.text,
                    phi_mau=self.validate_float(self.ids.phi_mau.text) or 0,
                    phi_size=self.validate_float(self.ids.phi_size.text) or 0,
                    phi_cat=self.validate_float(self.ids.phi_cat.text) or 0,
                    don_gia_von=float(self.ids.don_gia_von.text),
                    don_gia_goc=float(self.ids.don_gia_goc.text.replace('đ', '').replace(',', '')),
                    thanh_tien_goc=float(self.ids.thanh_tien_goc.text.replace('đ', '').replace(',', '')),
                    don_gia_ban=float(self.ids.don_gia_ban.text),
                    thanh_tien_ban=float(self.ids.thanh_tien_ban.text.replace('đ', '').replace(',', '')),
                    tien_coc=self.validate_float(self.ids.tien_coc.text) or 0,
                    cong_no_khach=float(self.ids.cong_no_khach.text.replace('đ', '').replace(',', '')),
                    ctv=self.ids.ctv.text,
                    hoa_hong=self.validate_float(self.ids.hoa_hong.text) or 0,
                    tien_hoa_hong=float(self.ids.tien_hoa_hong.text.replace('đ', '').replace(',', '')),
                    loi_giay=self.ids.loi_giay.text,
                    thung_bao=self.ids.thung_bao.text,
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
            self.ids.quy_cach_mm, self.ids.quy_cach_m, self.ids.quy_cach_mic,
            self.ids.cuon_cay, self.ids.so_luong, self.ids.phi_sl,
            self.ids.mau_keo, self.ids.phi_keo, self.ids.mau_sac,
            self.ids.phi_mau, self.ids.phi_size, self.ids.phi_cat,
            self.ids.don_gia_von, self.ids.don_gia_goc, self.ids.thanh_tien_goc,
            self.ids.don_gia_ban, self.ids.thanh_tien_ban, self.ids.tien_coc,
            self.ids.cong_no_khach, self.ids.ctv, self.ids.hoa_hong,
            self.ids.tien_hoa_hong, self.ids.loi_giay, self.ids.thung_bao,
            self.ids.loi_nhuan, self.ids.tien_ship, self.ids.loi_nhuan_rong
        ]
        self.clear_fields(fields_to_clear) 