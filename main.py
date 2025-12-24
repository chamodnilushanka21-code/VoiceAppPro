import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import speech_recognition as sr
from twilio.rest import Client
import random

# --- මෙතනට ඔයාගේ Twilio විස්තර දාන්න ---
account_sid = 'AC8b73786b6d379fba78d89afd2dbc1205' # ඔයාගේ Account SID එක
auth_token = '62cd316b6d38a17b7986414192fe80d3'   # ඔයාගේ Auth Token එක
twilio_number = '+1 802 802 9558'                    # ඔයාගේ Twilio Number එක
# ----------------------------------------

KV = '''
ScreenManager:
    LanguageScreen:
    RegScreen:
    OTPScreen:
    MainApp:

<LanguageScreen>:
    name: 'lang_screen'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'සිංහල'
            on_release: root.set_lang('si')
        Button:
            text: 'English'
            on_release: root.set_lang('en')

<RegScreen>:
    name: 'reg_screen'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: phone_input
            hint_text: 'Phone Number (+947...)'
        Button:
            text: 'Get OTP'
            on_release: root.send_otp()

<OTPScreen>:
    name: 'otp_screen'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: otp_input
            hint_text: 'Enter OTP'
        Button:
            text: 'Verify'
            on_release: root.verify_otp()

<MainApp>:
    name: 'main_app'
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: lb
            text: 'Listening...'
        Button:
            text: 'Speak'
            on_release: root.process()
'''

class LanguageScreen(Screen):
    def set_lang(self, lang):
        App.get_running_app().lang = lang
        self.manager.current = 'reg_screen'

class RegScreen(Screen):
    def send_otp(self):
        phone = self.ids.phone_input.text
        otp = str(random.randint(1000, 9999))
        App.get_running_app().otp = otp
        try:
            client = Client(account_sid, auth_token)
            client.messages.create(body=f'Your OTP is {otp}', from_=twilio_number, to=phone)
            self.manager.current = 'otp_screen'
        except:
            print("Error sending SMS")

class OTPScreen(Screen):
    def verify_otp(self):
        if self.ids.otp_input.text == App.get_running_app().otp:
            self.manager.current = 'main_app'

class MainApp(Screen):
    def process(self):
        # Voice Command Logic Here
        self.ids.lb.text = "Call logic goes here"

class VoiceProApp(App):
    lang = 'si'
    otp = ''
    def build(self):
        return Builder.load_string(KV)

if _name_ == '_main_':
    VoiceProApp().run()
