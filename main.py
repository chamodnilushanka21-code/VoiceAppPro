
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import speech_recognition as sr
from plyer import call
import random
import requests

# App Branding
PRIMARY_COLOR = (0.12, 0.58, 0.95, 1) # Professional Blue
Window.clearcolor = (0.05, 0.05, 0.08, 1) # Premium Dark

LANG_DATA = {
    'si': {
        'welcome': 'සාදරයෙන් පිළිගනිමු', 'reg': 'ලියාපදිංචි වන්න', 'phone': 'දුරකථන අංකය',
        'get_otp': 'OTP ලබාගන්න', 'verify': 'තහවුරු කරන්න', 'call': 'නම පවසන්න',
        'status': 'අසා සිටී...', 'err_otp': 'වැරදි OTP අංකයකි'
    },
    'en': {
        'welcome': 'Welcome Pro', 'reg': 'Register Now', 'phone': 'Phone Number',
        'get_otp': 'Get OTP', 'verify': 'Verify', 'call': 'Say Name',
        'status': 'Listening...', 'err_otp': 'Invalid OTP'
    }
}

class LanguageScreen(Screen):
    def set_lang(self, lang):
        App.get_running_app().lang = lang
        self.manager.current = 'reg_screen'

class RegScreen(Screen):
    def send_otp(self, phone):
        # Twilio API Configuration
        sid = 'ඔයාගේ_TWILIO_SID'
        token = 'ඔයාගේ_TWILIO_TOKEN'
        from_num = 'ඔයාගේ_TWILIO_NUMBER'
        
        otp = str(random.randint(1000, 9999))
        App.get_running_app().otp = otp
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
        data = {"From": from_num, "To": phone, "Body": f"Voice Dialer Pro Code: {otp}"}
        
        try:
            res = requests.post(url, data=data, auth=(sid, token))
            if res.status_code == 201: self.manager.current = 'otp_screen'
            else: self.ids.info.text = "Twilio Configuration Error!"
        except: self.ids.info.text = "Check Connection"

class OTPScreen(Screen):
    def check_otp(self, val):
        if val == App.get_running_app().otp: self.manager.current = 'main_app'
        else: self.ids.info.text = LANG_DATA[App.get_running_app().lang]['err_otp']

class MainApp(Screen):
    def start_listen(self):
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        ln = 'si-LK' if App.get_running_app().lang == 'si' else 'en-US'
        rec = sr.Recognizer()
        with sr.Microphone() as src:
            self.update_label(LANG_DATA[App.get_running_app().lang]['status'])
            try:
                audio = rec.listen(src, timeout=5)
                name = rec.recognize_google(audio, language=ln)
                self.make_call(name.lower())
            except: self.update_label("Retry...")

    def make_call(self, name):
        # Sample Contacts - Replace with real ones
        contacts = {"අම්මා": "0712345678", "mom": "0712345678"}
        for k, v in contacts.items():
            if k in name:
                call.makecall(tel=v)
                return
        self.update_label("Not Found")

    def update_label(self, txt):
        Clock.schedule_once(lambda dt: setattr(self.ids.lb, 'text', txt))

class VoiceProApp(App):
    lang = 'si'
    otp = ''
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LanguageScreen(name='lang_screen'))
        sm.add_widget(RegScreen(name='reg_screen'))
        sm.add_widget(OTPScreen(name='otp_screen'))
        sm.add_widget(MainApp(name='main_app'))
        return sm

if _name_ == '_main_':
    VoiceProApp().run()
