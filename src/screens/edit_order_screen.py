from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.app import MDApp
from datetime import datetime
from ..database.config import SessionLocal
from ..database.models import BangKeoInOrder, BangKeoOrder, TrucInOrder
from .bang_keo_in_tab import BangKeoInTab
from .bang_keo_tab import BangKeoTab
from .truc_in_tab import TrucInTab
from kivy.lang import Builder

Builder.load_string('''
<EditOrderScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_light
        spacing: 0
        
        MDTopAppBar:
            title: "Chỉnh sửa đơn hàng"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["content-save", lambda x: root.update_order()]]
            
        MDBoxLayout:
            id: content
            orientation: 'vertical'
            size_hint_y: 1
            padding: dp(10)
''')

class EditOrderScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_order = None
        self.order_type = None
        self.dialog = None
        
    def load_order(self, order, order_type):
        """Load order data into the form"""
        self.current_order = order
        self.order_type = order_type
        
        if order_type == "Băng keo in":
            self.load_bang_keo_in_order(order)
        elif order_type == "Băng keo":
            self.load_bang_keo_order(order)
        elif order_type == "Trục in":
            self.load_truc_in_order(order)
            
    def load_bang_keo_in_order(self, order):
        """Load Băng keo in order data"""
        tab = BangKeoInTab()
        tab.ids.ten_hang.text = order.ten_hang
        tab.ids.ten_khach_hang.text = order.ten_khach_hang
        tab.ids.ngay_du_kien.text = order.ngay_du_kien.strftime("%d/%m/%Y")
        tab.ids.quy_cach_mm.text = str(order.quy_cach_mm)
        tab.ids.quy_cach_m.text = str(order.quy_cach_m)
        tab.ids.quy_cach_mic.text = str(order.quy_cach_mic)
        tab.ids.cuon_cay.text = str(order.cuon_cay)
        tab.ids.so_luong.text = str(order.so_luong)
        tab.ids.phi_sl.text = str(order.phi_sl) if order.phi_sl else ""
        tab.ids.mau_keo.text = order.mau_keo or ""
        tab.ids.phi_keo.text = str(order.phi_keo) if order.phi_keo else ""
        tab.ids.mau_sac.text = order.mau_sac or ""
        tab.ids.phi_mau.text = str(order.phi_mau) if order.phi_mau else ""
        tab.ids.phi_size.text = str(order.phi_size) if order.phi_size else ""
        tab.ids.phi_cat.text = str(order.phi_cat) if order.phi_cat else ""
        tab.ids.don_gia_von.text = str(order.don_gia_von)
        tab.ids.don_gia_ban.text = str(order.don_gia_ban)
        tab.ids.tien_coc.text = str(order.tien_coc) if order.tien_coc else ""
        tab.ids.ctv.text = order.ctv or ""
        tab.ids.hoa_hong.text = str(order.hoa_hong) if order.hoa_hong else ""
        tab.ids.loi_giay.text = order.loi_giay or ""
        tab.ids.thung_bao.text = order.thung_bao or ""
        tab.ids.tien_ship.text = str(order.tien_ship) if order.tien_ship else ""
        
        # Trigger calculation
        tab.tinh_toan()
        
        # Replace current content with the loaded form
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(tab)
        
    def load_bang_keo_order(self, order):
        """Load Băng keo order data"""
        tab = BangKeoTab()
        tab.ids.ten_hang.text = order.ten_hang
        tab.ids.ten_khach_hang.text = order.ten_khach_hang
        tab.ids.ngay_du_kien.text = order.ngay_du_kien.strftime("%d/%m/%Y")
        tab.ids.quy_cach.text = order.quy_cach
        tab.ids.so_luong.text = str(order.so_luong)
        tab.ids.don_gia_goc.text = str(order.don_gia_goc)
        tab.ids.don_gia_ban.text = str(order.don_gia_ban)
        tab.ids.ten_ctv.text = order.ten_ctv or ""
        tab.ids.hoa_hong_ctv.text = str(order.hoa_hong_ctv) if order.hoa_hong_ctv else ""
        tab.ids.ghi_chu.text = order.ghi_chu or ""
        
        # Trigger calculation
        tab.tinh_toan()
        
        # Replace current content with the loaded form
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(tab)
        
    def load_truc_in_order(self, order):
        """Load Trục in order data"""
        tab = TrucInTab()
        tab.ids.ten_hang.text = order.ten_hang
        tab.ids.ten_khach_hang.text = order.ten_khach_hang
        tab.ids.ngay_du_kien.text = order.ngay_du_kien.strftime("%d/%m/%Y")
        tab.ids.quy_cach.text = order.quy_cach
        tab.ids.so_luong.text = str(order.so_luong)
        tab.ids.mau_sac.text = order.mau_sac or ""
        tab.ids.mau_keo.text = order.mau_keo or ""
        tab.ids.don_gia_goc.text = str(order.don_gia_goc)
        tab.ids.don_gia_ban.text = str(order.don_gia_ban)
        tab.ids.ctv.text = order.ctv or ""
        tab.ids.hoa_hong.text = str(order.hoa_hong) if order.hoa_hong else ""
        tab.ids.tien_ship.text = str(order.tien_ship) if order.tien_ship else ""
        
        # Trigger calculation
        tab.tinh_toan()
        
        # Replace current content with the loaded form
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(tab)
        
    def update_order(self):
        """Update the order in database"""
        try:
            with SessionLocal() as session:
                if self.order_type == "Băng keo in":
                    self.update_bang_keo_in_order(session)
                elif self.order_type == "Băng keo":
                    self.update_bang_keo_order(session)
                elif self.order_type == "Trục in":
                    self.update_truc_in_order(session)
                    
                session.commit()
                
            self.show_success("Đã cập nhật đơn hàng thành công!")
            self.go_back()
            
        except Exception as e:
            self.show_error(f"Lỗi khi cập nhật đơn hàng: {str(e)}")
            
    def update_bang_keo_in_order(self, session):
        """Update Băng keo in order"""
        tab = self.ids.content.children[0]
        order = session.query(BangKeoInOrder).get(self.current_order.id)
        
        order.ten_hang = tab.ids.ten_hang.text
        order.ten_khach_hang = tab.ids.ten_khach_hang.text
        order.ngay_du_kien = datetime.strptime(tab.ids.ngay_du_kien.text, "%d/%m/%Y")
        order.quy_cach_mm = float(tab.ids.quy_cach_mm.text)
        order.quy_cach_m = float(tab.ids.quy_cach_m.text)
        order.quy_cach_mic = float(tab.ids.quy_cach_mic.text)
        order.cuon_cay = float(tab.ids.cuon_cay.text)
        order.so_luong = float(tab.ids.so_luong.text)
        order.phi_sl = float(tab.ids.phi_sl.text) if tab.ids.phi_sl.text else 0
        order.mau_keo = tab.ids.mau_keo.text
        order.phi_keo = float(tab.ids.phi_keo.text) if tab.ids.phi_keo.text else 0
        order.mau_sac = tab.ids.mau_sac.text
        order.phi_mau = float(tab.ids.phi_mau.text) if tab.ids.phi_mau.text else 0
        order.phi_size = float(tab.ids.phi_size.text) if tab.ids.phi_size.text else 0
        order.phi_cat = float(tab.ids.phi_cat.text) if tab.ids.phi_cat.text else 0
        order.don_gia_von = float(tab.ids.don_gia_von.text)
        order.don_gia_goc = float(tab.ids.don_gia_goc.text.replace('đ', '').replace(',', ''))
        order.thanh_tien_goc = float(tab.ids.thanh_tien_goc.text.replace('đ', '').replace(',', ''))
        order.don_gia_ban = float(tab.ids.don_gia_ban.text)
        order.thanh_tien_ban = float(tab.ids.thanh_tien_ban.text.replace('đ', '').replace(',', ''))
        order.tien_coc = float(tab.ids.tien_coc.text) if tab.ids.tien_coc.text else 0
        order.cong_no_khach = float(tab.ids.cong_no_khach.text.replace('đ', '').replace(',', ''))
        order.ctv = tab.ids.ctv.text
        order.hoa_hong = float(tab.ids.hoa_hong.text) if tab.ids.hoa_hong.text else 0
        order.tien_hoa_hong = float(tab.ids.tien_hoa_hong.text.replace('đ', '').replace(',', ''))
        order.loi_giay = tab.ids.loi_giay.text
        order.thung_bao = tab.ids.thung_bao.text
        order.loi_nhuan = float(tab.ids.loi_nhuan.text.replace('đ', '').replace(',', ''))
        order.tien_ship = float(tab.ids.tien_ship.text) if tab.ids.tien_ship.text else 0
        order.loi_nhuan_rong = float(tab.ids.loi_nhuan_rong.text.replace('đ', '').replace(',', ''))
        
    def update_bang_keo_order(self, session):
        """Update Băng keo order"""
        tab = self.ids.content.children[0]
        order = session.query(BangKeoOrder).get(self.current_order.id)
        
        order.ten_hang = tab.ids.ten_hang.text
        order.ten_khach_hang = tab.ids.ten_khach_hang.text
        order.ngay_du_kien = datetime.strptime(tab.ids.ngay_du_kien.text, "%d/%m/%Y")
        order.quy_cach = tab.ids.quy_cach.text
        order.so_luong = float(tab.ids.so_luong.text)
        order.don_gia_goc = float(tab.ids.don_gia_goc.text)
        order.don_gia_ban = float(tab.ids.don_gia_ban.text)
        order.thanh_tien_goc = float(tab.ids.thanh_tien_goc.text.replace('đ', '').replace(',', ''))
        order.thanh_tien_ban = float(tab.ids.thanh_tien_ban.text.replace('đ', '').replace(',', ''))
        order.loi_nhuan = float(tab.ids.loi_nhuan.text.replace('đ', '').replace(',', ''))
        order.ten_ctv = tab.ids.ten_ctv.text
        order.hoa_hong_ctv = float(tab.ids.hoa_hong_ctv.text) if tab.ids.hoa_hong_ctv.text else 0
        order.thuc_thu_khach = float(tab.ids.thuc_thu_khach.text.replace('đ', '').replace(',', ''))
        order.ghi_chu = tab.ids.ghi_chu.text
        
    def update_truc_in_order(self, session):
        """Update Trục in order"""
        tab = self.ids.content.children[0]
        order = session.query(TrucInOrder).get(self.current_order.id)
        
        order.ten_hang = tab.ids.ten_hang.text
        order.ten_khach_hang = tab.ids.ten_khach_hang.text
        order.ngay_du_kien = datetime.strptime(tab.ids.ngay_du_kien.text, "%d/%m/%Y")
        order.quy_cach = tab.ids.quy_cach.text
        order.so_luong = float(tab.ids.so_luong.text)
        order.mau_sac = tab.ids.mau_sac.text
        order.mau_keo = tab.ids.mau_keo.text
        order.don_gia_goc = float(tab.ids.don_gia_goc.text)
        order.thanh_tien_goc = float(tab.ids.thanh_tien_goc.text.replace('đ', '').replace(',', ''))
        order.don_gia_ban = float(tab.ids.don_gia_ban.text)
        order.thanh_tien_ban = float(tab.ids.thanh_tien_ban.text.replace('đ', '').replace(',', ''))
        order.cong_no_khach = float(tab.ids.cong_no_khach.text.replace('đ', '').replace(',', ''))
        order.ctv = tab.ids.ctv.text
        order.hoa_hong = float(tab.ids.hoa_hong.text) if tab.ids.hoa_hong.text else 0
        order.tien_hoa_hong = float(tab.ids.tien_hoa_hong.text.replace('đ', '').replace(',', ''))
        order.loi_nhuan = float(tab.ids.loi_nhuan.text.replace('đ', '').replace(',', ''))
        order.tien_ship = float(tab.ids.tien_ship.text) if tab.ids.tien_ship.text else 0
        order.loi_nhuan_rong = float(tab.ids.loi_nhuan_rong.text.replace('đ', '').replace(',', ''))
        
    def delete_order(self):
        """Delete the order from database"""
        def confirm_delete(result):
            if not result:
                return
                
            try:
                with SessionLocal() as session:
                    if self.order_type == "Băng keo in":
                        order = session.query(BangKeoInOrder).get(self.current_order.id)
                    elif self.order_type == "Băng keo":
                        order = session.query(BangKeoOrder).get(self.current_order.id)
                    elif self.order_type == "Trục in":
                        order = session.query(TrucInOrder).get(self.current_order.id)
                        
                    session.delete(order)
                    session.commit()
                    
                self.show_success("Đã xóa đơn hàng thành công!")
                self.go_back()
                
            except Exception as e:
                self.show_error(f"Lỗi khi xóa đơn hàng: {str(e)}")
                
        self.show_confirm_dialog(
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa đơn hàng này?",
            confirm_delete
        )
        
    def show_confirm_dialog(self, title, text, callback):
        """Show confirmation dialog"""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="HỦY",
                        theme_text_color="Custom",
                        text_color=MDApp.get_running_app().theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="XÓA",
                        on_release=lambda x: [callback(True), self.dialog.dismiss()]
                    )
                ]
            )
        self.dialog.open()
        
    def show_success(self, message):
        """Show success message"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Thành công",
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="ĐÓNG",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.title = "Thành công"
            self.dialog.text = message
        self.dialog.open()
        
    def show_error(self, message):
        """Show error message"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Lỗi",
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="ĐÓNG",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.title = "Lỗi"
            self.dialog.text = message
        self.dialog.open()
        
    def go_back(self):
        """Return to history screen"""
        self.manager.current = 'history' 