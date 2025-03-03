from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty, StringProperty
from datetime import datetime
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog

class BaseInputTab(MDScreen):
    """Base class for input tabs"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        
    def show_date_picker(self, date_field):
        """Show date picker dialog"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, range: self.on_date_save(value, date_field))
        date_dialog.open()
        
    def on_date_save(self, value, date_field):
        """Handle date selection"""
        if value:
            date_field.text = value.strftime("%d/%m/%Y")
            
    def show_error(self, message):
        """Show error message"""
        Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            bg_color=(0.8, 0, 0, 1)
        ).open()
        
    def show_success(self, message):
        """Show success message"""
        Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            bg_color=(0.2, 0.8, 0.2, 1)
        ).open()
        
    def validate_float(self, text):
        """Validate float input"""
        try:
            if text:
                value = float(text)
                if value < 0:
                    return None
                return value
            return 0.0
        except ValueError:
            return None
            
    def validate_required_fields(self, fields):
        """Validate required fields"""
        # Handle dictionary format
        if isinstance(fields, dict):
            for field_id, name in fields.items():
                field = self.ids.get(field_id)
                if not field or not field.text:
                    self.show_error(f"Vui lòng nhập {name}")
                    return False
            return True
        
        # Handle list of tuples format
        for field, name in fields:
            if not field.text:
                self.show_error(f"Vui lòng nhập {name}")
                return False
        return True
        
    def format_currency(self, value):
        """Format number as currency"""
        try:
            return f"{float(value):,.0f}đ" if value else "0đ"
        except:
            return "0đ"
            
    def clear_fields(self, fields):
        """Clear all fields"""
        for field in fields:
            field.text = ""
            
    def calculate_total(self, quantity, price):
        """Calculate total amount"""
        try:
            return float(quantity) * float(price)
        except:
            return 0 