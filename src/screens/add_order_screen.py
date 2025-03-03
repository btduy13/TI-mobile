from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from datetime import datetime
from kivy.properties import BooleanProperty, StringProperty
from ..services.database_service import DatabaseService
from kivy.clock import Clock

from .bang_keo_in_tab import BangKeoInTab
from .bang_keo_tab import BangKeoTab
from .truc_in_tab import TrucInTab

Builder.load_string('''
<Tab>:
    MDLabel:
        id: label
        text: root.title
        halign: 'center'
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color if root.selected else (0, 0, 0, .5)
        bold: root.selected

<AddOrderScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_light
        spacing: 0
        
        MDTopAppBar:
            title: "Thêm đơn hàng mới"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            
        MDTabs:
            id: tabs
            height: dp(48)
            size_hint_y: None
            background_color: app.theme_cls.bg_light
            text_color_normal: 0, 0, 0, .5
            text_color_active: app.theme_cls.primary_color
            indicator_color: app.theme_cls.primary_color
            tab_hint_x: True
            on_tab_switch: root.on_tab_switch(*args)
            
        ScreenManager:
            id: tab_content
            size_hint_y: 1
''')

class Tab(FloatLayout, MDTabsBase):
    """Class for tabs"""
    title = StringProperty()
    selected = BooleanProperty(False)

class AddOrderScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_service = DatabaseService()
        self.selected_date = None
        self.current_tab = None
        self.bang_keo_in_tab = None
        self.bang_keo_tab = None
        self.truc_in_tab = None
        self.tabs_created = False
        
    def show_date_picker(self):
        """Hiển thị date picker để chọn ngày dự kiến"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()
        
    def on_save_date(self, instance, value, date_range):
        """Xử lý khi chọn ngày từ date picker"""
        self.selected_date = value
        self.ids.ngay_du_kien_field.text = value.strftime("%d/%m/%Y")
        
    def save_order(self):
        """Lưu đơn hàng mới"""
        if not self.selected_date or not self.ids.trang_thai_field.text:
            Snackbar(
                text="Vui lòng nhập đầy đủ thông tin",
                snackbar_x="10dp",
                snackbar_y="10dp",
            ).open()
            return
            
        try:
            self.db_service.create_don_hang(
                ngay_du_kien=self.selected_date,
                trang_thai=self.ids.trang_thai_field.text,
                ghi_chu=self.ids.ghi_chu_field.text
            )
            self.go_back()
        except Exception as e:
            Snackbar(
                text=f"Lỗi khi lưu đơn hàng: {str(e)}",
                snackbar_x="10dp",
                snackbar_y="10dp",
            ).open()
            
    def on_enter(self):
        """Called when screen is entered"""
        # Schedule the setup to ensure widgets are ready
        Clock.schedule_once(self.setup_screen)
        
    def setup_screen(self, dt):
        """Setup screen content"""
        if not self.tabs_created:
            # Create tabs
            self.bang_keo_in_tab = BangKeoInTab(name="bang_keo_in")
            self.bang_keo_tab = BangKeoTab(name="bang_keo")
            self.truc_in_tab = TrucInTab(name="truc_in")
            
            # Add screens to screen manager
            self.ids.tab_content.add_widget(self.bang_keo_in_tab)
            self.ids.tab_content.add_widget(self.bang_keo_tab)
            self.ids.tab_content.add_widget(self.truc_in_tab)
            
            # Add tabs
            tabs = [
                {"title": "Băng keo in", "screen": "bang_keo_in"},
                {"title": "Băng keo", "screen": "bang_keo"},
                {"title": "Trục in", "screen": "truc_in"}
            ]
            
            # Add new tabs
            for tab in tabs:
                tab_item = Tab(title=tab["title"])
                self.ids.tabs.add_widget(tab_item)
            
            # Show first tab content
            self.ids.tab_content.current = "bang_keo_in"
            self.tabs_created = True
            
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Handle tab switch"""
        if tab_text == "Băng keo in":
            self.ids.tab_content.current = "bang_keo_in"
        elif tab_text == "Băng keo":
            self.ids.tab_content.current = "bang_keo"
        elif tab_text == "Trục in":
            self.ids.tab_content.current = "truc_in"
            
    def go_back(self):
        """Quay lại màn hình danh sách"""
        self.manager.current = 'order_list' 