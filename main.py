from kivy.config import Config
Config.set('graphics', 'width', 360 )
Config.set('graphics', 'height', 600)

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
#import numpy as np
import math
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.chip import MDChip


class MainScreen(Screen):
    def metric_to_bmi(self, kg, cm):
        self.display_bmi  = str(kg / ((cm/100)**2))
        print(self.display_bmi)

    def convert_ft_to_cm(self, ft):
        return ft * 30.48

    def convert_inch_to_cm(self, inch):
        return inch * 2.54

    def convert_lbs_to_kg(self, lbs):
        return lbs / 2.205

    def imperial_to_bmi(self, ft, inch, lbs):
        kg = self.convert_lbs_to_kg(lbs)
        cm = self.convert_ft_to_cm(ft) + self.convert_inch_to_cm(inch)
        return self.metric_to_bmi(kg, cm)

class WindowManager(ScreenManager):
    pass

class BMICalculator(MDApp):

    display_bmi = ""

    def __init__(self, **kwargs):
        super(BMICalculator, self).__init__(**kwargs)
        #place the red dot 10 meters out from the middle of the field

    def test(self):
        print('test')

    def metric_to_bmi(self, kg, cm):
        self.display_bmi  = str(kg / (cm**2))

    def convert_ft_to_cm(self, ft):
        return ft * 30.48

    def convert_inch_to_cm(self, inch):
        return inch * 2.54

    def convert_lbs_to_kg(self, lbs):
        return lbs / 2.205

    def imperial_to_bmi(self, ft, inch, lbs):
        kg = self.convert_lbs_to_kg(lbs)
        cm = self.convert_ft_to_cm(ft) + self.convert_inch_to_cm(inch)
        return self.metric_to_bmi(kg, cm)



BMICalculator().run()
