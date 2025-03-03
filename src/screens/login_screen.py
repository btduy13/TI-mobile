from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar

Builder.load_string('''
<LoginScreen>:
    username: username
    password: password
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        Widget:
            size_hint_y: 0.2
            
        MDLabel:
            text: "Tape Inventory"
            halign: "center"
            font_style: "H4"
            size_hint_y: 0.2
            
        MDTextField:
            id: username
            hint_text: "Tên đăng nhập"
            helper_text: "Nhập tên đăng nhập"
            helper_text_mode: "on_error"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            
        MDTextField:
            id: password
            hint_text: "Mật khẩu"
            helper_text: "Nhập mật khẩu"
            helper_text_mode: "on_error"
            password: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            
        MDRaisedButton:
            text: "ĐĂNG NHẬP"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_release: root.login()
            
        Widget:
            size_hint_y: 0.2
''')

class LoginScreen(MDScreen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def login(self):
        """Handle login logic"""
        username = self.username.text
        password = self.password.text
        
        # TODO: Add proper authentication
        if username and password:  # Temporary simple validation
            # Switch to main screen first
            self.manager.current = 'main'
            # Then switch to order list in content manager
            content_manager = self.manager.get_screen('main').ids.content_manager
            content_manager.current = 'order_list'
        else:
            Snackbar(
                text="Vui lòng nhập tên đăng nhập và mật khẩu",
                snackbar_x="10dp",
                snackbar_y="10dp",
            ).open() 