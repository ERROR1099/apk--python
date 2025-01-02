import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

import requests
import socket
import json
import dns.resolver
from ipwhois import IPWhois
import speedtest
import ping3
import uuid
import hashlib
import base64
import ssl
import whois
import traceroute
import concurrent.futures
import platform
import subprocess
import re
import threading

class NetworkToolsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Network Tools'
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Speed Test Section
        speed_layout = BoxLayout(orientation='vertical', spacing=5)
        self.speed_label = Label(text='Network Speed Test', size_hint_y=None, height=40)
        self.speed_progress = ProgressBar(max=100, size_hint_y=None, height=20)
        self.speed_result_label = Label(text='', size_hint_y=None, height=100)
        
        speed_button = Button(text='Start Speed Test', on_press=self.run_speed_test, size_hint_y=None, height=40)
        
        speed_layout.add_widget(self.speed_label)
        speed_layout.add_widget(speed_button)
        speed_layout.add_widget(self.speed_progress)
        speed_layout.add_widget(self.speed_result_label)
        
        # Ping Section
        ping_layout = BoxLayout(spacing=10)
        self.ping_input = TextInput(multiline=False, hint_text='Enter host to ping', size_hint_x=0.7)
        ping_button = Button(text='Ping', on_press=self.run_ping, size_hint_x=0.3)
        ping_layout.add_widget(self.ping_input)
        ping_layout.add_widget(ping_button)
        
        self.ping_result_label = Label(text='Ping results will appear here')
        
        # Traceroute Section
        traceroute_layout = BoxLayout(spacing=10)
        self.traceroute_input = TextInput(multiline=False, hint_text='Enter destination', size_hint_x=0.7)
        traceroute_button = Button(text='Traceroute', on_press=self.run_traceroute, size_hint_x=0.3)
        traceroute_layout.add_widget(self.traceroute_input)
        traceroute_layout.add_widget(traceroute_button)
        
        self.traceroute_result_label = Label(text='Traceroute results will appear here')
        
        layout.add_widget(speed_layout)
        layout.add_widget(ping_layout)
        layout.add_widget(self.ping_result_label)
        layout.add_widget(traceroute_layout)
        layout.add_widget(self.traceroute_result_label)
        
        self.add_widget(layout)
    
    def run_speed_test(self, instance):
        def test_speed():
            try:
                st = speedtest.Speedtest()
                self.speed_progress.value = 25
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                self.speed_progress.value = 50
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                self.speed_progress.value = 75
                ping = st.results.ping
                self.speed_progress.value = 100
                
                result_text = f"Download: {download_speed:.2f} Mbps\n"
                result_text += f"Upload: {upload_speed:.2f} Mbps\n"
                result_text += f"Ping: {ping:.2f} ms"
                
                Clock.schedule_once(lambda dt: setattr(self.speed_result_label, 'text', result_text))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.speed_result_label, 'text', f"Speed Test Error: {str(e)}"))
        
        # Reset progress and result
        self.speed_progress.value = 0
        self.speed_result_label.text = 'Running speed test...'
        
        # Run speed test in a separate thread
        threading.Thread(target=test_speed).start()
    
    def run_ping(self, instance):
        host = self.ping_input.text.strip()
        try:
            response_time = ping3.ping(host)
            if response_time is not None:
                self.ping_result_label.text = f"Ping to {host}: {response_time * 1000:.2f} ms"
            else:
                self.ping_result_label.text = f"Ping to {host} failed"
        except Exception as e:
            self.ping_result_label.text = f"Ping Error: {str(e)}"
    
    def run_traceroute(self, instance):
        host = self.traceroute_input.text.strip()
        try:
            # Use platform-specific traceroute command
            if platform.system().lower() == 'windows':
                cmd = ['tracert', host]
            else:
                cmd = ['traceroute', host]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            self.traceroute_result_label.text = result.stdout
        except Exception as e:
            self.traceroute_result_label.text = f"Traceroute Error: {str(e)}"

class SecurityToolsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Security Tools'
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # SSL Certificate Checker
        ssl_layout = BoxLayout(spacing=10)
        self.ssl_input = TextInput(multiline=False, hint_text='Enter website URL', size_hint_x=0.7)
        ssl_button = Button(text='Check SSL', on_press=self.check_ssl_cert, size_hint_x=0.3)
        ssl_layout.add_widget(self.ssl_input)
        ssl_layout.add_widget(ssl_button)
        
        self.ssl_result_label = Label(text='SSL certificate details will appear here')
        
        # Hash Generator
        hash_layout = BoxLayout(spacing=10)
        self.hash_input = TextInput(multiline=False, hint_text='Enter text to hash', size_hint_x=0.7)
        hash_button = Button(text='Generate Hashes', on_press=self.generate_hashes, size_hint_x=0.3)
        hash_layout.add_widget(self.hash_input)
        hash_layout.add_widget(hash_button)
        
        self.hash_result_label = Label(text='Generated hashes will appear here')
        
        # UUID Generator
        uuid_button = Button(text='Generate UUID', on_press=self.generate_uuid)
        self.uuid_result_label = Label(text='Generated UUID will appear here')
        
        layout.add_widget(ssl_layout)
        layout.add_widget(self.ssl_result_label)
        layout.add_widget(hash_layout)
        layout.add_widget(self.hash_result_label)
        layout.add_widget(uuid_button)
        layout.add_widget(self.uuid_result_label)
        
        self.add_widget(layout)
    
    def check_ssl_cert(self, instance):
        url = self.ssl_input.text.strip()
        try:
            hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
            cert = ssl.get_server_certificate((hostname, 443))
            x509 = ssl.PEM_cert_to_DER_cert(cert)
            
            # Use OpenSSL to parse certificate details
            from OpenSSL import crypto
            x509_obj = crypto.load_certificate(crypto.FILETYPE_ASN1, x509)
            
            subject = x509_obj.get_subject()
            issuer = x509_obj.get_issuer()
            
            result_text = f"Subject: {subject.CN}\n"
            result_text += f"Issuer: {issuer.CN}\n"
            result_text += f"Version: {x509_obj.get_version()}\n"
            result_text += f"Serial Number: {x509_obj.get_serial_number()}"
            
            self.ssl_result_label.text = result_text
        except Exception as e:
            self.ssl_result_label.text = f"SSL Check Error: {str(e)}"
    
    def generate_hashes(self, instance):
        text = self.hash_input.text
        
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        sha1_hash = hashlib.sha1(text.encode()).hexdigest()
        sha256_hash = hashlib.sha256(text.encode()).hexdigest()
        base64_encoded = base64.b64encode(text.encode()).decode()
        
        result_text = f"MD5: {md5_hash}\n"
        result_text += f"SHA1: {sha1_hash}\n"
        result_text += f"SHA256: {sha256_hash}\n"
        result_text += f"Base64: {base64_encoded}"
        
        self.hash_result_label.text = result_text
    
    def generate_uuid(self, instance):
        new_uuid = str(uuid.uuid4())
        self.uuid_result_label.text = f"Generated UUID: {new_uuid}"

class IPInfoApp(App):
    def build(self):
        # Main tabbed panel
        tp = TabbedPanel()
        tp.default_tab_text = 'IP Info'
        
        # IP Info Tab (original functionality)
        ip_info_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input section
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.input_field = TextInput(
            multiline=False, 
            hint_text='Enter IP or URL', 
            size_hint_x=0.7
        )
        search_button = Button(
            text='Get Info', 
            size_hint_x=0.3, 
            on_press=self.fetch_ip_info
        )
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(search_button)
        
        # Result scroll view
        self.result_scroll = ScrollView()
        self.result_label = Label(
            text='Enter an IP or URL to get information', 
            size_hint_y=None, 
            text_size=(400, None),
            halign='left',
            valign='top'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        
        # Add widgets to IP Info layout
        ip_info_layout.add_widget(input_layout)
        ip_info_layout.add_widget(self.result_scroll)
        
        # Set default tab content
        tp.default_tab.content = ip_info_layout
        
        # Add Network Tools Tab
        network_tools_tab = NetworkToolsTab()
        tp.add_widget(network_tools_tab)
        
        # Add Security Tools Tab
        security_tools_tab = SecurityToolsTab()
        tp.add_widget(security_tools_tab)
        
        return tp
    
    def fetch_ip_info(self, instance):
        input_text = self.input_field.text.strip()
        
        try:
            # Resolve IP if URL is provided
            if not self.is_valid_ip(input_text):
                input_text = socket.gethostbyname(input_text)
            
            # Fetch IP information
            ip_info = self.get_comprehensive_ip_info(input_text)
            
            # Format the information
            formatted_info = self.format_ip_info(ip_info)
            
            # Update result label
            self.result_label.text = formatted_info
        
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"
    
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
        
        # WHOIS Info
        whois = ip_info['WHOIS']
        formatted += "WHOIS INFORMATION:\n"
        formatted += f"Network Name: {whois.get('network', {}).get('name', 'N/A')}\n"
        formatted += f"CIDR: {whois.get('network', {}).get('cidr', 'N/A')}\n"
        formatted += f"Range: {whois.get('network', {}).get('range', 'N/A')}\n\n"
        
        # DNS Info
        dns_info = ip_info['DNS']
        formatted += "DNS INFORMATION:\n"
        formatted += "A Records:\n"
        for record in dns_info.get('A Records', ['No A Records']):
            formatted += f"- {record}\n"
        formatted += "\nMX Records:\n"
        for record in dns_info.get('MX Records', ['No MX Records']):
            formatted += f"- {record}\n"
        
        return formatted

def main():
    IPInfoApp().run()

if __name__ == '__main__':
    main()
