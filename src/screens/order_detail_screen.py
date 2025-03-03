from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDSeparator
from kivy.lang import Builder
from kivy.properties import NumericProperty
from datetime import datetime
from ..services.database_service import DatabaseService, DatabaseError
from kivymd.uix.snackbar import Snackbar

Builder.load_string('''
<OrderDetailScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Chi tiết đơn hàng"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["pencil", lambda x: root.edit_order()], ["delete", lambda x: root.delete_order()]]
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)
            
            MDLabel:
                id: order_header
                text: "Đơn hàng #0"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
                
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(120)
                spacing: dp(10)
                padding: [0, dp(10)]
                
                MDLabel:
                    id: order_date
                    text: "Ngày đặt: --/--/----"
                
                MDLabel:
                    id: expected_date
                    text: "Ngày dự kiến: --/--/----"
                    
                MDLabel:
                    id: status
                    text: "Trạng thái: ---"
                    
                MDLabel:
                    id: note
                    text: "Ghi chú: ---"
            
            MDSeparator:
                height: dp(1)
            
            MDLabel:
                text: "Chi tiết đơn hàng"
                font_style: "H6"
                size_hint_y: None
                height: dp(40)
            
            ScrollView:
                MDList:
                    id: detail_list
                    padding: dp(0)
                    spacing: dp(5)
        
        MDFloatingActionButton:
            icon: "plus"
            pos_hint: {"right": 0.95, "y": 0.05}
            on_release: root.add_order_detail()
''')

class OrderDetailScreen(MDScreen):
    order_id = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_service = DatabaseService()
        self.current_order = None
        self.dialog = None
        
    def on_enter(self):
        """Called when screen is displayed"""
        if not self.order_id:
            self.show_error("Không có thông tin đơn hàng")
            return
            
        try:
            self.load_order_details()
        except DatabaseError as e:
            self.show_error(str(e))
        
    def load_order_details(self):
        """Load order details from database"""
        try:
            self.current_order = self.db_service.get_don_hang(self.order_id)
            if not self.current_order:
                self.show_error("Không tìm thấy đơn hàng")
                return
            
            # Update header information
            self.ids.order_header.text = f"Đơn hàng #{self.current_order.id}"
            self.ids.order_date.text = f"Ngày đặt: {self.current_order.ngay_dat.strftime('%d/%m/%Y')}"
            self.ids.expected_date.text = f"Ngày dự kiến: {self.current_order.ngay_du_kien.strftime('%d/%m/%Y')}"
            self.ids.status.text = f"Trạng thái: {self.current_order.trang_thai}"
            self.ids.note.text = f"Ghi chú: {self.current_order.ghi_chu or '---'}"
            
            # Load order details
            detail_list = self.ids.detail_list
            detail_list.clear_widgets()
            
            if not self.current_order.chi_tiet:
                detail_list.add_widget(
                    MDLabel(
                        text="Chưa có chi tiết đơn hàng",
                        halign="center",
                        theme_text_color="Secondary"
                    )
                )
            else:
                for detail in self.current_order.chi_tiet:
                    item = TwoLineIconListItem(
                        text=f"{detail.ten_hang} - {detail.quy_cach}",
                        secondary_text=f"SL: {detail.so_luong:,} - Đơn giá: {detail.don_gia:,.0f}đ",
                        on_release=lambda x, d=detail: self.show_item_detail(d)
                    )
                    item.add_widget(IconLeftWidget(icon="package-variant"))
                    detail_list.add_widget(item)
                    
        except DatabaseError as e:
            self.show_error(f"Lỗi khi tải thông tin đơn hàng: {str(e)}")
            
    def add_order_detail(self):
        """Show dialog to add new order detail"""
        self.show_add_item_dialog()
        
    def show_add_item_dialog(self):
        """Show dialog to add new item"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Thêm chi tiết đơn hàng",
                type="custom",
                content_cls=OrderItemForm(),
                buttons=[
                    MDRaisedButton(
                        text="HỦY",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="THÊM",
                        on_release=lambda x: self.add_order_item()
                    ),
                ],
            )
        self.dialog.open()
        
    def add_order_item(self):
        """Add new item to order"""
        try:
            form = self.dialog.content_cls
            
            # Validate required fields
            required_fields = [
                (form.ten_hang, "Tên hàng"),
                (form.so_luong, "Số lượng"),
                (form.don_gia, "Đơn giá"),
                (form.quy_cach, "Quy cách"),
                (form.mau_sac, "Màu sắc"),
                (form.mau_keo, "Màu keo")
            ]
            
            for field, name in required_fields:
                if not field.text:
                    self.show_error(f"Vui lòng nhập {name}")
                    return
                    
            try:
                so_luong = int(form.so_luong.text)
                if so_luong <= 0:
                    self.show_error("Số lượng phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error("Số lượng không hợp lệ")
                return
                
            try:
                don_gia = float(form.don_gia.text)
                if don_gia <= 0:
                    self.show_error("Đơn giá phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error("Đơn giá không hợp lệ")
                return
            
            item = self.db_service.add_chi_tiet_don_hang(
                self.order_id,
                form.ten_hang.text,
                so_luong,
                don_gia,
                form.quy_cach.text,
                form.mau_sac.text,
                form.mau_keo.text
            )
            
            if item:
                self.dialog.dismiss()
                self.load_order_details()
                Snackbar(
                    text="Đã thêm chi tiết đơn hàng",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    bg_color=(0.2, 0.8, 0.2, 1)  # Green background for success
                ).open()
            else:
                self.show_error("Không thể thêm chi tiết đơn hàng")
                
        except ValueError as e:
            self.show_error(str(e))
        except DatabaseError as e:
            self.show_error(str(e))
            
    def show_item_detail(self, item):
        """Show detailed information for an order item"""
        if not self.dialog:
            content = MDBoxLayout(orientation='vertical', spacing='10dp', padding='20dp')
            content.add_widget(MDLabel(text=f"Tên hàng: {item.ten_hang}"))
            content.add_widget(MDLabel(text=f"Số lượng: {item.so_luong:,}"))
            content.add_widget(MDLabel(text=f"Đơn giá: {item.don_gia:,.0f}đ"))
            content.add_widget(MDLabel(text=f"Quy cách: {item.quy_cach}"))
            content.add_widget(MDLabel(text=f"Màu sắc: {item.mau_sac}"))
            content.add_widget(MDLabel(text=f"Màu keo: {item.mau_keo}"))
            content.add_widget(MDLabel(text=f"Thành tiền: {item.thanh_tien:,.0f}đ"))
            
            self.dialog = MDDialog(
                title="Chi tiết đơn hàng",
                type="custom",
                content_cls=content,
                buttons=[
                    MDRaisedButton(
                        text="ĐÓNG",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()
        
    def edit_order(self):
        """Navigate to edit order screen"""
        # TODO: Implement edit order screen
        pass
        
    def delete_order(self):
        """Delete current order"""
        confirm_dialog = MDDialog(
            title="Xác nhận xóa",
            text="Bạn có chắc chắn muốn xóa đơn hàng này?",
            buttons=[
                MDRaisedButton(
                    text="HỦY",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="XÓA",
                    on_release=lambda x: self.confirm_delete(confirm_dialog)
                )
            ]
        )
        confirm_dialog.open()
        
    def confirm_delete(self, dialog):
        """Handle order deletion confirmation"""
        try:
            self.db_service.delete_don_hang(self.order_id)
            dialog.dismiss()
            self.go_back()
        except Exception as e:
            dialog.dismiss()
            self.show_error(str(e))
            
    def show_error(self, message):
        """Show error message in a snackbar"""
        Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.9,
            bg_color=(0.8, 0, 0, 1)  # Red background for errors
        ).open()
        
    def go_back(self):
        """Return to order list screen"""
        self.manager.current = 'order_list'

class OrderItemForm(MDBoxLayout):
    """Form for adding/editing order items"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '10dp'
        self.size_hint_y = None
        self.height = "400dp"
        
        # Add input fields
        self.ten_hang = MDTextField(
            hint_text="Tên hàng",
            helper_text="Nhập tên hàng",
            helper_text_mode="on_error",
            required=True
        )
        self.so_luong = MDTextField(
            hint_text="Số lượng",
            helper_text="Nhập số lượng",
            helper_text_mode="on_error",
            required=True,
            input_filter="int"
        )
        self.don_gia = MDTextField(
            hint_text="Đơn giá",
            helper_text="Nhập đơn giá",
            helper_text_mode="on_error",
            required=True,
            input_filter="float"
        )
        self.quy_cach = MDTextField(
            hint_text="Quy cách",
            helper_text="Nhập quy cách",
            helper_text_mode="on_error",
            required=True
        )
        self.mau_sac = MDTextField(
            hint_text="Màu sắc",
            helper_text="Nhập màu sắc",
            helper_text_mode="on_error",
            required=True
        )
        self.mau_keo = MDTextField(
            hint_text="Màu keo",
            helper_text="Nhập màu keo",
            helper_text_mode="on_error",
            required=True
        )
        
        # Add fields to form
        self.add_widget(self.ten_hang)
        self.add_widget(self.so_luong)
        self.add_widget(self.don_gia)
        self.add_widget(self.quy_cach)
        self.add_widget(self.mau_sac)
        self.add_widget(self.mau_keo) 