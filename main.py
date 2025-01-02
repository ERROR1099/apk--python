import kivy
kivy.require('2.2.1')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

import requests
import socket
import dns.resolver
from ipwhois import IPWhois
import speedtest
import ping3
import uuid
import hashlib
import base64
import threading
import matplotlib.pyplot as plt
import seaborn as sns
import io
import traceback  # Added for better error handling

class IPInfoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ip_info'
        
        # Main layout
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = MDLabel(
            text='IP FETCH',
            font_style='H4',
            halign='center',
            theme_text_color='Primary'
        )
        layout.add_widget(title)
        
        # IP/URL Input
        self.ip_input = MDTextField(
            hint_text='Enter IP or URL',
            helper_text='Example: 8.8.8.8 or google.com',
            helper_text_mode='on_error',
            required=True
        )
        layout.add_widget(self.ip_input)
        
        # Fetch Button
        fetch_button = MDRaisedButton(
            text='Get IP Info',
            pos_hint={'center_x': 0.5},
            on_release=self.fetch_ip_info
        )
        layout.add_widget(fetch_button)
        
        # Result Card
        self.result_card = MDCard(
            orientation='vertical',
            padding=10,
            spacing=10,
            size_hint=(0.9, None),
            height=400,
            pos_hint={'center_x': 0.5}
        )
        
        # Result Label
        self.result_label = MDLabel(
            text='IP information will appear here',
            theme_text_color='Secondary'
        )
        self.result_card.add_widget(self.result_label)
        
        layout.add_widget(self.result_card)
        
        self.add_widget(layout)
    
    def fetch_ip_info(self, instance):
        input_text = self.ip_input.text.strip()
        
        # Validate input
        if not input_text:
            Snackbar(text="Please enter an IP or URL").open()
            return
        
        # Start loading
        progress = MDProgressBar(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.8
        )
        self.result_card.add_widget(progress)
        
        def fetch_info():
            try:
                # Resolve IP if URL is provided
                resolved_ip = input_text
                if not self.is_valid_ip(input_text):
                    resolved_ip = socket.gethostbyname(input_text)
                
                # Fetch comprehensive IP info
                ip_info = self.get_comprehensive_ip_info(resolved_ip)
                
                # Update UI on main thread
                kivy.clock.Clock.schedule_once(
                    lambda dt: self.update_result_card(ip_info), 0
                )
            except Exception as error:
                # Capture full error traceback
                error_message = traceback.format_exc()
                kivy.clock.Clock.schedule_once(
                    lambda dt: self.show_error(error_message), 0
                )
        
        # Run in separate thread
        threading.Thread(target=fetch_info).start()
    
    def is_valid_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def get_comprehensive_ip_info(self, ip):
        # Geolocation info
        geo_response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        
        # WHOIS info
        whois_info = IPWhois(ip).lookup_rdap()
        
        # DNS info
        try:
            dns_info = {
                'A Records': [str(rdata) for rdata in dns.resolver.resolve(ip, 'A')],
                'MX Records': [str(rdata) for rdata in dns.resolver.resolve(ip, 'MX')]
            }
        except:
            dns_info = {'DNS': 'No DNS records found'}
        
        return {
            'Geolocation': geo_response,
            'WHOIS': whois_info,
            'DNS': dns_info
        }
    
    def update_result_card(self, ip_info):
        # Remove progress bar
        if self.result_card.children and isinstance(self.result_card.children[0], MDProgressBar):
            self.result_card.remove_widget(self.result_card.children[0])
        
        # Format result text
        result_text = self.format_ip_info(ip_info)
        
        # Update result label
        self.result_label.text = result_text
    
    def format_ip_info(self, ip_info):
        formatted = "IP/URL INFORMATION:\n\n"
        
        # Geolocation Info
        geo = ip_info['Geolocation']
        formatted += "GEOLOCATION:\n"
        formatted += f"IP: {geo.get('ip', 'N/A')}\n"
        formatted += f"City: {geo.get('city', 'N/A')}\n"
        formatted += f"Region: {geo.get('region', 'N/A')}\n"
        formatted += f"Country: {geo.get('country_name', 'N/A')}\n"
        formatted += f"Latitude: {geo.get('latitude', 'N/A')}\n"
        formatted += f"Longitude: {geo.get('longitude', 'N/A')}\n"
        formatted += f"ISP: {geo.get('org', 'N/A')}\n\n"
        
        return formatted
    
    def show_error(self, error_message):
        dialog = MDDialog(
            title='Error',
            text=error_message,
            buttons=[
                MDRaisedButton(
                    text='OK',
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

class NetworkToolsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'network_tools'
        
        # Main layout
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Speed Test Section
        speed_layout = MDBoxLayout(orientation='vertical', spacing=10)
        speed_title = MDLabel(
            text='Network Speed Test',
            font_style='H6',
            halign='center',
            theme_text_color='Primary'
        )
        
        self.speed_result_label = MDLabel(
            text='Run a speed test to check your network',
            theme_text_color='Secondary',
            halign='center'
        )
        
        speed_button = MDRaisedButton(
            text='Start Speed Test',
            pos_hint={'center_x': 0.5},
            on_release=self.run_speed_test
        )
        
        speed_layout.add_widget(speed_title)
        speed_layout.add_widget(speed_button)
        speed_layout.add_widget(self.speed_result_label)
        
        layout.add_widget(speed_layout)
        
        self.add_widget(layout)
    
    def run_speed_test(self, instance):
        def test_speed():
            try:
                st = speedtest.Speedtest()
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                ping = st.results.ping
                
                result_text = f"Download: {download_speed:.2f} Mbps\n"
                result_text += f"Upload: {upload_speed:.2f} Mbps\n"
                result_text += f"Ping: {ping:.2f} ms"
                
                kivy.clock.Clock.schedule_once(
                    lambda dt: setattr(
                        self.speed_result_label, 
                        'text', 
                        result_text
                    ), 
                    0
                )
            except Exception as error:
                error_message = traceback.format_exc()
                kivy.clock.Clock.schedule_once(
                    lambda dt: setattr(
                        self.speed_result_label, 
                        'text', 
                        f"Speed Test Error: {error_message}"
                    ), 
                    0
                )
        
        # Run speed test in a separate thread
        threading.Thread(target=test_speed).start()

class IPFetchApp(MDApp):
    def build(self):
        # Set app theme
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        # Create screen manager
        screen_manager = MDScreenManager()
        
        # Create screens
        ip_info_screen = IPInfoScreen()
        network_tools_screen = NetworkToolsScreen()
        
        # Add screens to manager
        screen_manager.add_widget(ip_info_screen)
        screen_manager.add_widget(network_tools_screen)
        
        # Bottom Navigation
        bottom_nav = MDBottomNavigation()
        
        # IP Info Navigation Item
        ip_info_item = MDBottomNavigationItem(
            icon='information',
            text='IP Info',
            name='ip_info'
        )
        ip_info_item.bind(on_tab_press=lambda x: screen_manager.current_screen.name)
        
        # Network Tools Navigation Item
        network_tools_item = MDBottomNavigationItem(
            icon='network',
            text='Network Tools',
            name='network_tools'
        )
        network_tools_item.bind(on_tab_press=lambda x: screen_manager.current_screen.name)
        
        bottom_nav.add_widget(ip_info_item)
        bottom_nav.add_widget(network_tools_item)
        
        return screen_manager

def main():
    IPFetchApp().run()

if __name__ == '__main__':
    main()
