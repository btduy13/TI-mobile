from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from datetime import datetime, timedelta
from functools import partial
from threading import Thread
from ..services.database_service import DatabaseService, DatabaseError
from ..database.models import BangKeoInOrder, TrucInOrder, BangKeoOrder
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from ..database.config import DATABASE_URL, SessionLocal
from kivymd.theming import ThemableBehavior
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

Builder.load_string('''
<Tab>:
    MDLabel:
        id: label
        text: root.tab_label_text
        halign: 'center'
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color if root.selected else (0, 0, 0, .5)
        bold: root.selected

<HistoryScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_light
        spacing: 0
        
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
            
        MDCard:
            id: filter_card
            orientation: "vertical"
            size_hint_y: None
            height: dp(120)
            padding: dp(8)
            margin: dp(8)
            radius: dp(4)
            elevation: 1
            
            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(8)
                size_hint_y: None
                height: dp(48)
                
                MDTextField:
                    id: search_field
                    hint_text: "Tìm kiếm theo tên"
                    helper_text_mode: "on_focus"
                    size_hint_x: 0.7
                    on_text: root.update_search_text(self.text)
                
                MDIconButton:
                    icon: "magnify"
                    pos_hint: {"center_y": .5}
                    on_release: root.apply_filters()
                    
                MDIconButton:
                    icon: "filter-remove"
                    pos_hint: {"center_y": .5}
                    on_release: root.clear_filters()
            
            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(8)
                size_hint_y: None
                height: dp(48)
                
                MDTextField:
                    id: start_date
                    hint_text: "Từ ngày"
                    readonly: True
                    size_hint_x: 0.5
                    on_focus: if self.focus: root.show_date_picker("start")
                
                MDTextField:
                    id: end_date
                    hint_text: "Đến ngày"
                    readonly: True
                    size_hint_x: 0.5
                    on_focus: if self.focus: root.show_date_picker("end")
            
        ScrollView:
            do_scroll_x: False
            effect_cls: "ScrollEffect"
            
            MDList:
                id: history_list
                padding: [dp(4), 0, dp(4), dp(4)]
                spacing: dp(2)
                    
        MDBoxLayout:
            id: loading_container
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .5}
''')

class Tab(FloatLayout, MDTabsBase):
    """Class for tabs"""
    selected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_label_text = kwargs.get('tab_label_text', '')

class HistoryScreen(MDScreen):
    """Screen for displaying order history."""
    search_text = StringProperty("")
    start_date_obj = ObjectProperty(None)
    end_date_obj = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_service = DatabaseService()
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.current_tab = 'all'  # Default tab
        self.loading_spinner = None
        # Set default date range to last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.start_date_obj = start_date
        self.end_date_obj = end_date
        # Bind event to search text
        self.bind(search_text=self.on_search_text_changed)
        
    def on_search_text_changed(self, instance, value):
        # Don't reload immediately to avoid too many queries
        pass
        
    def update_search_text(self, text):
        self.search_text = text
    
    def show_date_picker(self, date_type):
        """Show date picker for start or end date"""
        def on_save(instance, value, date_range):
            if date_type == "start":
                self.start_date_obj = value
                self.ids.start_date.text = value.strftime("%d/%m/%Y")
            else:
                self.end_date_obj = value
                self.ids.end_date.text = value.strftime("%d/%m/%Y")
        
        default_date = self.start_date_obj if date_type == "start" else self.end_date_obj
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=on_save)
        date_dialog.open()
        
    def apply_filters(self):
        """Apply current filters and reload data"""
        self.load_history()
        
    def clear_filters(self):
        """Clear all filters"""
        self.search_text = ""
        self.ids.search_field.text = ""
        # Reset date range to last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.start_date_obj = start_date
        self.end_date_obj = end_date
        self.ids.start_date.text = ""
        self.ids.end_date.text = ""
        # Reload data
        self.load_history()
        
    def show_loading(self):
        """Display loading spinner while fetching data."""
        if hasattr(self, 'loading_container'):
            self.remove_widget(self.loading_container)
            
        self.loading_container = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            padding=dp(10),
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(0.9, 0.9, 0.9, 0.7),
            radius=[dp(10),]
        )
        
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            active=True,
            palette=[
                [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],  # Light green
                [0.3568627450980392, 0.6078431372549019, 0.8352941176470589, 1],  # Light blue
                [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],  # Pink
                [0.8823529411764706, 0.6745098039215687, 0.2980392156862745, 1],  # Orange
            ]
        )
        
        loading_label = MDLabel(
            text="Đang tải...",
            halign="left",
            theme_text_color="Secondary",
            font_style="Body1"
        )
        
        self.loading_container.add_widget(spinner)
        self.loading_container.add_widget(loading_label)
        self.add_widget(self.loading_container)
        
    def hide_loading(self, *args):
        """Hide loading spinner"""
        if hasattr(self, 'loading_container'):
            self.remove_widget(self.loading_container)
        
    def open_nav_drawer(self):
        """Open the navigation drawer"""
        main_screen = self.manager.get_screen("main")
        nav_drawer = main_screen.ids.nav_drawer
        nav_drawer.set_state("open")
        
    def on_enter(self):
        """Called when screen is entered"""
        self.setup_tabs()
        # Set default date range display
        if self.start_date_obj and not self.ids.start_date.text:
            self.ids.start_date.text = self.start_date_obj.strftime("%d/%m/%Y")
        if self.end_date_obj and not self.ids.end_date.text:
            self.ids.end_date.text = self.end_date_obj.strftime("%d/%m/%Y")
        self.load_history()
        
    def setup_tabs(self):
        """Setup the filter tabs"""
        tabs = self.ids.tabs
        # Instead of clear_widgets, we'll remove each tab individually
        while len(tabs.get_tab_list()):
            tabs.remove_widget(tabs.get_tab_list()[0])
            
        # Add new tabs with corrected spacing
        tab_data = [
            ("Tất cả", "all"),  # Removed extra space
            ("Băng keo in", "bang_keo_in"),
            ("Trục in", "truc_in"),
            ("Băng keo", "bang_keo")
        ]
        
        for text, tab_id in tab_data:
            tab = Tab(tab_label_text=text)
            tab.selected = (tab_id == self.current_tab)
            tabs.add_widget(tab)
        
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Handle tab switching"""
        # Update tab appearance
        for tab in instance_tabs.get_tab_list():
            tab.selected = (tab == instance_tab)
            
        # Update current tab and load data
        tab_map = {
            "Tất cả": "all",
            "Băng keo in": "bang_keo_in",
            "Trục in": "truc_in",
            "Băng keo": "bang_keo"
        }
        self.current_tab = tab_map.get(tab_text, "all")
        self.load_history()
        
    def load_history(self):
        """Load order history based on current tab and filters"""
        self.show_loading()
        # Use Clock to schedule the actual loading
        Clock.schedule_once(self._load_history_async)
        
    def _load_history_async(self, *args):
        """Asynchronously load history data with filters applied"""
        try:
            session = self.Session()
            history_list = self.ids.history_list
            history_list.clear_widgets()
            
            # Apply date range filter if provided
            if self.start_date_obj:
                start_date = datetime.combine(self.start_date_obj, datetime.min.time())
            else:
                start_date = datetime.now() - timedelta(days=30)
                
            if self.end_date_obj:
                end_date = datetime.combine(self.end_date_obj, datetime.max.time())
            else:
                end_date = datetime.now()
            
            # Load orders based on the current tab with filters
            if self.current_tab == "all":
                # Load all types of orders with filters
                bang_keo_in_query = session.query(BangKeoInOrder).filter(
                    BangKeoInOrder.thoi_gian.between(start_date, end_date)
                )
                truc_in_query = session.query(TrucInOrder).filter(
                    TrucInOrder.thoi_gian.between(start_date, end_date)
                )
                bang_keo_query = session.query(BangKeoOrder).filter(
                    BangKeoOrder.thoi_gian.between(start_date, end_date)
                )
                
                # Apply search filter if provided
                if self.search_text:
                    bang_keo_in_query = bang_keo_in_query.filter(
                        or_(
                            BangKeoInOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            BangKeoInOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                    truc_in_query = truc_in_query.filter(
                        or_(
                            TrucInOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            TrucInOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                    bang_keo_query = bang_keo_query.filter(
                        or_(
                            BangKeoOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            BangKeoOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                
                # Get results ordered by date
                bang_keo_in = bang_keo_in_query.order_by(BangKeoInOrder.thoi_gian.desc()).limit(50).all()
                truc_in = truc_in_query.order_by(TrucInOrder.thoi_gian.desc()).limit(50).all()
                bang_keo = bang_keo_query.order_by(BangKeoOrder.thoi_gian.desc()).limit(50).all()
                
                Clock.schedule_once(lambda dt: self.add_orders_to_list(bang_keo_in, "Băng keo in"))
                Clock.schedule_once(lambda dt: self.add_orders_to_list(truc_in, "Trục in"))
                Clock.schedule_once(lambda dt: self.add_orders_to_list(bang_keo, "Băng keo"))
                
            elif self.current_tab == "bang_keo_in":
                query = session.query(BangKeoInOrder).filter(
                    BangKeoInOrder.thoi_gian.between(start_date, end_date)
                )
                
                # Apply search filter if provided
                if self.search_text:
                    query = query.filter(
                        or_(
                            BangKeoInOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            BangKeoInOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                
                orders = query.order_by(BangKeoInOrder.thoi_gian.desc()).all()
                Clock.schedule_once(lambda dt: self.add_orders_to_list(orders, "Băng keo in"))
                
            elif self.current_tab == "truc_in":
                query = session.query(TrucInOrder).filter(
                    TrucInOrder.thoi_gian.between(start_date, end_date)
                )
                
                # Apply search filter if provided
                if self.search_text:
                    query = query.filter(
                        or_(
                            TrucInOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            TrucInOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                
                orders = query.order_by(TrucInOrder.thoi_gian.desc()).all()
                Clock.schedule_once(lambda dt: self.add_orders_to_list(orders, "Trục in"))
                
            elif self.current_tab == "bang_keo":
                query = session.query(BangKeoOrder).filter(
                    BangKeoOrder.thoi_gian.between(start_date, end_date)
                )
                
                # Apply search filter if provided
                if self.search_text:
                    query = query.filter(
                        or_(
                            BangKeoOrder.ten_khach_hang.ilike(f'%{self.search_text}%'),
                            BangKeoOrder.ten_hang.ilike(f'%{self.search_text}%')
                        )
                    )
                
                orders = query.order_by(BangKeoOrder.thoi_gian.desc()).all()
                Clock.schedule_once(lambda dt: self.add_orders_to_list(orders, "Băng keo"))
                
        except Exception as e:
            error_message = str(e)
            Clock.schedule_once(lambda dt, error=error_message: self.show_error(f"Lỗi khi tải lịch sử: {error}"))
        finally:
            session.close()
            Clock.schedule_once(self.hide_loading)
            
    def add_orders_to_list(self, orders, order_type):
        """Add orders to the list widget"""
        history_list = self.ids.history_list
        
        if not orders:
            if len(history_list.children) == 0:  # Only show if no other orders
                item = MDBoxLayout(
                    orientation='vertical',
                    padding=dp(16),
                    spacing=dp(8)
                )
                item.add_widget(
                    MDLabel(
                        text="Không có đơn hàng nào",
                        halign="center",
                        theme_text_color="Secondary",
                        font_style="H6"
                    )
                )
                item.add_widget(
                    MDLabel(
                        text="Chọn tab khác để xem thêm",
                        halign="center",
                        theme_text_color="Secondary",
                        font_style="Caption"
                    )
                )
                history_list.add_widget(item)
            return
            
        for order in orders:
            status = "Đã giao" if order.da_giao else "Chưa giao"
            payment = "Đã tất toán" if order.da_tat_toan else "Chưa tất toán"
            
            item = ThreeLineIconListItem(
                IconLeftWidget(
                    icon="check-circle" if order.da_giao else "clock-outline",
                    theme_text_color="Custom",
                    text_color=(0, 0.7, 0, 1) if order.da_giao else (0.7, 0.7, 0, 1)
                ),
                text=f"[b]{order_type} - {order.id}[/b]",
                secondary_text=f"[color=666666]{order.ten_khach_hang} - {order.ten_hang}[/color]",
                tertiary_text=(
                    f"[color=666666]Ngày: {order.thoi_gian.strftime('%d/%m/%Y')} - "
                    f"{status} - {payment}[/color]"
                ),
                on_release=lambda x, o=order, t=order_type: self.show_order_details(o, t)
            )
            history_list.add_widget(item)
            
    def show_order_details(self, order, order_type):
        """Show order details in a dialog."""
        app = MDApp.get_running_app()
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(400)
        )
        
        # Create scrollable content
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        details_box = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        details_box.bind(minimum_height=details_box.setter('height'))
        
        # Add order details with improved formatting
        details = [
            f"Mã đơn: {order.id}",
            f"Khách hàng: {order.ten_khach_hang}",
            f"Tên hàng: {order.ten_hang}",
            f"Ngày đặt: {order.thoi_gian.strftime('%d/%m/%Y')}",
            f"Ngày dự kiến: {order.ngay_du_kien.strftime('%d/%m/%Y')}"
        ]
        
        # Add type-specific details
        if order_type == "Băng keo in":
            details.extend([
                f"\nQuy cách: {order.quy_cach_mm}mm x {order.quy_cach_m}m x {order.quy_cach_mic}mic",
                f"Cuộn/Cây: {order.cuon_cay}"
            ])
        else:
            details.append(f"\nQuy cách: {order.quy_cach}")
            
        # Add financial information
        details.extend([
            f"\nSố lượng: {order.so_luong:,}",
            f"Đơn giá bán: {order.don_gia_ban:,.0f}đ",
            f"Thành tiền: {order.thanh_tien_ban:,.0f}đ",
            f"Công nợ: {order.cong_no_khach:,.0f}đ"
        ])
        
        # Add additional fields if available
        if hasattr(order, 'mau_keo'):
            details.append(f"Màu keo: {order.mau_keo}")
        if hasattr(order, 'mau_sac'):
            details.append(f"Màu sắc: {order.mau_sac}")
        
        for detail in details:
            label = MDLabel(
                text=detail,
                theme_text_color="Secondary" if ":" in detail else "Primary",
                font_style="Body1",
                size_hint_y=None,
                height=dp(30)
            )
            details_box.add_widget(label)
        
        scroll.add_widget(details_box)
        content.add_widget(scroll)
        
        dialog = MDDialog(
            title=f"Chi tiết {order_type}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Chỉnh sửa",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                    on_release=lambda x: [self.edit_order(order, order_type), dialog.dismiss()]
                ),
                MDFlatButton(
                    text="Xóa",
                    theme_text_color="Custom",
                    text_color=(0.8, 0, 0, 1),  # Red color
                    on_release=lambda x: [self.delete_order(order, order_type), dialog.dismiss()]
                ),
                MDFlatButton(
                    text="Đóng",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
            size_hint=(.8, None),
            height=dp(500)
        )
        dialog.open()
        
    def edit_order(self, order, order_type):
        """Open edit order screen"""
        edit_screen = self.manager.get_screen('edit_order')
        edit_screen.load_order(order, order_type)
        self.manager.current = 'edit_order'
        
    def delete_order(self, order, order_type):
        """Delete order"""
        def confirm_delete(result):
            if not result:
                return
                
            try:
                with SessionLocal() as session:
                    if order_type == "Băng keo in":
                        db_order = session.query(BangKeoInOrder).get(order.id)
                    elif order_type == "Băng keo":
                        db_order = session.query(BangKeoOrder).get(order.id)
                    elif order_type == "Trục in":
                        db_order = session.query(TrucInOrder).get(order.id)
                        
                    if db_order:
                        session.delete(db_order)
                        session.commit()
                        self.show_success("Đã xóa đơn hàng thành công!")
                        self.load_history()  # Reload the list after deletion
                    else:
                        self.show_error("Không tìm thấy đơn hàng để xóa!")
                    
            except Exception as e:
                self.show_error(f"Lỗi khi xóa đơn hàng: {str(e)}")
                
        dialog = MDDialog(
            title="Xác nhận xóa",
            text="Bạn có chắc chắn muốn xóa đơn hàng này?",
            buttons=[
                MDFlatButton(
                    text="HỦY",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="XÓA",
                    on_release=lambda x: [confirm_delete(True), dialog.dismiss()]
                )
            ]
        )
        dialog.open()
        
    def show_success(self, message):
        """Show success message"""
        dialog = MDDialog(
            title="Thành công",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="ĐÓNG",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
        
    def show_error(self, message):
        """Show error message"""
        app = MDApp.get_running_app()
        dialog = MDDialog(
            title="Lỗi",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="ĐÓNG",
                    on_release=lambda x: dialog.dismiss(),
                    md_bg_color=app.theme_cls.primary_color
                )
            ],
            radius=[dp(20), dp(20), dp(20), dp(20)]
        )
        dialog.open() 