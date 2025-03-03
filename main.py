from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen

from src.screens.login_screen import LoginScreen
from src.screens.order_list_screen import OrderListScreen
from src.screens.add_order_screen import AddOrderScreen
from src.screens.order_detail_screen import OrderDetailScreen
from src.screens.history_screen import HistoryScreen
from src.screens.edit_order_screen import EditOrderScreen
from src.database.init_db import init_database

KV = '''
<ContentNavigationDrawer>
    ScrollView:
        MDList:
            OneLineIconListItem:
                text: "Danh sách đơn hàng"
                on_release: 
                    root.nav_drawer.set_state("close")
                    app.switch_screen("order_list")
                IconLeftWidget:
                    icon: "format-list-bulleted"
                    
            OneLineIconListItem:
                text: "Lịch sử đơn hàng"
                on_release:
                    root.nav_drawer.set_state("close")
                    app.switch_screen("history")
                IconLeftWidget:
                    icon: "history"

<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Quản lý đơn hàng"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
            
        MDNavigationLayout:
            ScreenManager:
                id: content_manager
                
                OrderListScreen:
                    name: "order_list"
                    
                AddOrderScreen:
                    name: "add_order"
                    
                OrderDetailScreen:
                    name: "order_detail"
                    
                HistoryScreen:
                    name: "history"
                    
                EditOrderScreen:
                    name: "edit_order"
            
            MDNavigationDrawer:
                id: nav_drawer
                radius: (0, 16, 16, 0)
                
                ContentNavigationDrawer:
                    nav_drawer: nav_drawer

MDScreen:
    ScreenManager:
        id: screen_manager
        
        LoginScreen:
            name: "login"
            
        MainScreen:
            name: "main"

'''

class ContentNavigationDrawer(MDBoxLayout):
    nav_drawer = ObjectProperty()

class MainScreen(MDScreen):
    pass

class TapeInventoryApp(MDApp):
    def build(self):
        # Initialize database
        init_database()
        
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.root.ids.screen_manager.current = "login"
        
    def switch_screen(self, screen_name):
        """Switch to specified screen in content manager"""
        main_screen = self.root.ids.screen_manager.get_screen("main")
        content_manager = main_screen.ids.content_manager
        content_manager.current = screen_name

if __name__ == "__main__":
    TapeInventoryApp().run() 