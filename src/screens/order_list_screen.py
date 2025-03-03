from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from datetime import datetime
from ..services.database_service import DatabaseService, DatabaseError

Builder.load_string('''
<OrderListScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        ScrollView:
            do_scroll_x: False
            
            MDList:
                id: order_list
                padding: dp(20)
                spacing: dp(10)
        
        MDFloatingActionButton:
            icon: "plus"
            pos_hint: {"right": 0.95, "y": 0.05}
            on_release: root.add_new_order()
''')

class OrderListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_service = DatabaseService()
        
    def on_enter(self):
        """Called when the screen is displayed"""
        # Schedule the load_orders call to ensure widgets are initialized
        Clock.schedule_once(lambda dt: self.load_orders())
        
    def load_orders(self, *args):
        """Load all orders from database"""
        try:
            orders = self.db_service.get_all_don_hang()
            
            # Get the order list widget
            order_list = None
            for child in self.walk():
                if isinstance(child, MDList):
                    order_list = child
                    break
                    
            if not order_list:
                print("Error: Could not find order list widget")
                return
                
            order_list.clear_widgets()
            
            if not orders:
                # Add a message when no orders are found
                item = TwoLineIconListItem(
                    IconLeftWidget(
                        icon="information"
                    ),
                    text="Không có đơn hàng nào",
                    secondary_text="Nhấn nút + để thêm đơn hàng mới"
                )
                order_list.add_widget(item)
                return
            
            for order in orders:
                status_icon = "check-circle" if order.da_giao else "clock-outline"
                item = TwoLineIconListItem(
                    IconLeftWidget(
                        icon=status_icon
                    ),
                    text=f"Đơn hàng #{order.id}",
                    secondary_text=f"Ngày đặt: {order.ngay_dat.strftime('%d/%m/%Y')} - {order.trang_thai}",
                    on_release=lambda x, order_id=order.id: self.view_order_details(order_id)
                )
                order_list.add_widget(item)
        except DatabaseError as e:
            print(f"Error loading orders: {e}")
            # Add an error message to the list
            order_list = None
            for child in self.walk():
                if isinstance(child, MDList):
                    order_list = child
                    break
                    
            if order_list:
                order_list.clear_widgets()
                item = TwoLineIconListItem(
                    IconLeftWidget(
                        icon="alert"
                    ),
                    text="Lỗi tải dữ liệu",
                    secondary_text="Vui lòng thử lại sau"
                )
                order_list.add_widget(item)
            
    def add_new_order(self):
        """Navigate to add new order screen"""
        self.manager.current = 'add_order'
        
    def view_order_details(self, order_id):
        """Navigate to order details screen"""
        detail_screen = self.manager.get_screen('order_detail')
        detail_screen.order_id = order_id
        self.manager.current = 'order_detail'
        
    def toggle_nav_drawer(self):
        """Toggle navigation drawer"""
        # TODO: Implement navigation drawer
        pass 