from kivy.lang import Builder
from .base_input_tab import BaseInputTab
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
from ..database.models import BangKeoOrder
from ..database.config import SessionLocal

Builder.load_string('''
<BangKeoTab>:
    name: "bang_keo"
    
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
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(15)
                    spacing: dp(10)
                    md_bg_color: 1, 1, 1, 1
                    radius: [5]
                    elevation: 1
                    
                    MDLabel:
                        text: "Thông tin cơ bản"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDTextField:
                        id: ten_hang
                        hint_text: "Tên hàng"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        size_hint_y: None
                        height: dp(48)
                        
                    MDTextField:
                        id: ten_khach_hang
                        hint_text: "Tên khách hàng"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        size_hint_y: None
                        height: dp(48)
                        
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(48)
                        spacing: dp(10)
                        
                        MDTextField:
                            id: ngay_du_kien
                            hint_text: "Ngày dự kiến"
                            readonly: True
                            size_hint_x: 0.8
                            
                        MDIconButton:
                            icon: "calendar"
                            on_release: root.show_date_picker(ngay_du_kien)
                            size_hint_x: 0.2
                            pos_hint: {"center_y": .5}
                
                # Thông tin sản phẩm
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(15)
                    spacing: dp(10)
                    md_bg_color: 1, 1, 1, 1
                    radius: [5]
                    elevation: 1
                    
                    MDLabel:
                        text: "Thông tin sản phẩm"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDTextField:
                        id: quy_cach
                        hint_text: "Quy cách"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        size_hint_y: None
                        height: dp(48)
                        
                    MDTextField:
                        id: so_luong
                        hint_text: "Số lượng"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(48)
                        on_text: root.auto_calculate()
                
                # Giá cả
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(15)
                    spacing: dp(10)
                    md_bg_color: 1, 1, 1, 1
                    radius: [5]
                    elevation: 1
                    
                    MDLabel:
                        text: "Giá cả"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDTextField:
                        id: don_gia_goc
                        hint_text: "Đơn giá gốc"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(48)
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: don_gia_ban
                        hint_text: "Đơn giá bán"
                        helper_text: "Bắt buộc"
                        helper_text_mode: "on_error"
                        required: True
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(48)
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: thanh_tien
                        hint_text: "Thành tiền"
                        readonly: True
                        size_hint_y: None
                        height: dp(48)
                        
                    MDTextField:
                        id: thanh_tien_ban
                        hint_text: "Thành tiền bán"
                        readonly: True
                        size_hint_y: None
                        height: dp(48)
                        
                    MDTextField:
                        id: loi_nhuan
                        hint_text: "Lợi nhuận"
                        readonly: True
                        mode: "rectangle"
                        size_hint_y: None
                        height: "48dp"
                        
                    MDTextField:
                        id: tien_ship
                        hint_text: "Tiền ship"
                        mode: "rectangle"
                        size_hint_y: None
                        height: "48dp"
                        input_filter: "float"
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: loi_nhuan_rong
                        hint_text: "Lợi nhuận ròng"
                        readonly: True
                        mode: "rectangle"
                        size_hint_y: None
                        height: "48dp"
                
                # CTV và hoa hồng
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(15)
                    spacing: dp(10)
                    md_bg_color: 1, 1, 1, 1
                    radius: [5]
                    elevation: 1
                    
                    MDLabel:
                        text: "CTV và hoa hồng"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDTextField:
                        id: ten_ctv
                        hint_text: "Tên CTV"
                        size_hint_y: None
                        height: dp(48)
                        
                    MDTextField:
                        id: hoa_hong_ctv
                        hint_text: "Hoa hồng CTV"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(48)
                        on_text: root.auto_calculate()
                        
                    MDTextField:
                        id: thuc_thu_khach
                        hint_text: "Thực thu khách"
                        readonly: True
                        size_hint_y: None
                        height: dp(48)
                
                # Thông tin thêm
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(15)
                    spacing: dp(10)
                    md_bg_color: 1, 1, 1, 1
                    radius: [5]
                    elevation: 1
                    
                    MDLabel:
                        text: "Thông tin thêm"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                        
                    MDTextField:
                        id: ghi_chu
                        hint_text: "Ghi chú"
                        multiline: True
                        size_hint_y: None
                        height: dp(100)
                
                # Nút bấm
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(56)
                    spacing: dp(10)
                    padding: [0, dp(10), 0, dp(10)]
                    
                    MDRaisedButton:
                        text: "Tính toán"
                        on_release: root.tinh_toan()
                        size_hint_x: 0.5
                        
                    MDRaisedButton:
                        text: "Lưu đơn hàng"
                        on_release: root.luu_don_hang()
                        md_bg_color: app.theme_cls.primary_color
                        size_hint_x: 0.5
''')

class BangKeoTab(BaseInputTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def auto_calculate(self):
        """Tự động tính toán khi thay đổi giá trị"""
        try:
            if (self.ids.so_luong.text and 
                self.ids.don_gia_goc.text and 
                self.ids.don_gia_ban.text):
                self.tinh_toan()
        except:
            pass
    
    def tinh_toan(self):
        """Tính toán các giá trị dựa trên dữ liệu nhập vào"""
        try:
            # Lấy giá trị từ các trường
            so_luong = self.validate_float(self.ids.so_luong.text)
            don_gia_goc = self.validate_float(self.ids.don_gia_goc.text)
            don_gia_ban = self.validate_float(self.ids.don_gia_ban.text)
            hoa_hong_ctv = self.validate_float(self.ids.hoa_hong_ctv.text)
            tien_ship = self.validate_float(self.ids.tien_ship.text)
            
            # Tính toán
            if so_luong and don_gia_goc:
                thanh_tien = so_luong * don_gia_goc
                self.ids.thanh_tien.text = self.format_currency(thanh_tien)
            
            if so_luong and don_gia_ban:
                thanh_tien_ban = so_luong * don_gia_ban
                self.ids.thanh_tien_ban.text = self.format_currency(thanh_tien_ban)
            
            if so_luong and don_gia_goc and don_gia_ban:
                loi_nhuan = (so_luong * don_gia_ban) - (so_luong * don_gia_goc)
                self.ids.loi_nhuan.text = self.format_currency(loi_nhuan)
                
                # Tính lợi nhuận ròng = lợi nhuận - hoa hồng CTV - tiền ship
                loi_nhuan_rong = loi_nhuan - (hoa_hong_ctv or 0) - (tien_ship or 0)
                self.ids.loi_nhuan_rong.text = self.format_currency(loi_nhuan_rong)
            
            if so_luong and don_gia_ban and hoa_hong_ctv:
                thuc_thu_khach = (so_luong * don_gia_ban) - (hoa_hong_ctv or 0)
                self.ids.thuc_thu_khach.text = self.format_currency(thuc_thu_khach)
                
        except Exception as e:
            print(f"Lỗi khi tính toán: {str(e)}")
    
    def luu_don_hang(self):
        """Lưu đơn hàng vào cơ sở dữ liệu"""
        # Kiểm tra các trường bắt buộc
        required_fields = {
            'ten_hang': 'Tên hàng',
            'ten_khach_hang': 'Tên khách hàng',
            'ngay_du_kien': 'Ngày dự kiến',
            'quy_cach': 'Quy cách',
            'so_luong': 'Số lượng',
            'don_gia_goc': 'Đơn giá gốc',
            'don_gia_ban': 'Đơn giá bán'
        }
        
        if not self.validate_required_fields(required_fields):
            return
        
        try:
            # Lấy giá trị từ các trường
            ten_hang = self.ids.ten_hang.text
            ten_khach_hang = self.ids.ten_khach_hang.text
            ngay_du_kien = datetime.strptime(self.ids.ngay_du_kien.text, "%d/%m/%Y")
            quy_cach = self.ids.quy_cach.text
            so_luong = float(self.ids.so_luong.text)
            don_gia_goc = float(self.ids.don_gia_goc.text)
            don_gia_ban = float(self.ids.don_gia_ban.text)
            ten_ctv = self.ids.ten_ctv.text
            hoa_hong_ctv = float(self.ids.hoa_hong_ctv.text) if self.ids.hoa_hong_ctv.text else 0
            tien_ship = float(self.ids.tien_ship.text) if self.ids.tien_ship.text else 0
            
            # Tính toán các giá trị
            thanh_tien = so_luong * don_gia_goc
            thanh_tien_ban = so_luong * don_gia_ban
            loi_nhuan = thanh_tien_ban - thanh_tien
            thuc_thu_khach = thanh_tien_ban - hoa_hong_ctv
            loi_nhuan_rong = loi_nhuan - hoa_hong_ctv - tien_ship
            
            # Tạo đối tượng đơn hàng mới
            with SessionLocal() as session:
                new_order = BangKeoOrder(
                    ten_hang=ten_hang,
                    ten_khach_hang=ten_khach_hang,
                    ngay_du_kien=ngay_du_kien,
                    quy_cach=quy_cach,
                    so_luong=so_luong,
                    don_gia_goc=don_gia_goc,
                    don_gia_ban=don_gia_ban,
                    thanh_tien=thanh_tien,
                    thanh_tien_ban=thanh_tien_ban,
                    loi_nhuan=loi_nhuan,
                    ctv=ten_ctv,
                    hoa_hong=hoa_hong_ctv,
                    tien_hoa_hong=hoa_hong_ctv,
                    cong_no_khach=thuc_thu_khach,
                    tien_ship=tien_ship,
                    loi_nhuan_rong=loi_nhuan_rong
                )
                
                session.add(new_order)
                session.commit()
            
                # Hiển thị thông báo thành công
                self.show_success(f"Đơn hàng {new_order.id} đã được lưu thành công!")
            
            # Xóa form
            self.xoa_form()
            
        except Exception as e:
            self.show_error(f"Lỗi khi lưu đơn hàng: {str(e)}")
    
    def xoa_form(self):
        """Xóa tất cả các trường nhập liệu"""
        fields = [
            'ten_hang', 'ten_khach_hang', 'ngay_du_kien', 'quy_cach', 
            'so_luong', 'don_gia_goc', 'don_gia_ban', 'thanh_tien', 
            'thanh_tien_ban', 'loi_nhuan', 'ten_ctv', 'hoa_hong_ctv', 
            'thuc_thu_khach', 'tien_ship', 'loi_nhuan_rong'
        ]
        
        self.clear_fields(fields) 