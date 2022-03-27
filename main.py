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
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.vkeyboard import VKeyboard

class MainScreen(Screen):

    height_units_1 = StringProperty("ft")
    height_units_2 = StringProperty("in")
    height_1_bool = BooleanProperty(False)
    system = "imperial"
    weight_units = StringProperty('lbs')
    display_bmi = StringProperty("")

    def calculate_bmi(self):
        # do the checks first

        if self.system == "imperial":
            # we are using the imperial system
            # so we need ft, in, and lbs
            ft = self.ids.height_1.text
            inches = self.ids.height_2.text
            lbs = self.ids.weight.text

            # need all three
            if ((len(ft) == 0) | (len(inches) == 0) | (len(lbs) == 0)):
                print('bad')

            else:
                # calculate the bmi
                # convert to floats
                ft = float(ft)
                inches = float(inches)
                lbs = float(lbs)
                self.display_bmi = self.imperial_to_bmi(ft, inches, lbs)

        else:
            # its not imperial so its the metric system
            cm = self.ids.height_2.text
            kgs = self.ids.weight.text

            if ((len(cm) == 0) | (len(kgs) == 0)):
                # we are missing some data
                print('bad')
            else:
                # we have everything we need
                # convert to floats
                cm = float(cm)
                kgs = float(kgs)
                self.display_bmi = self.metric_to_bmi(cm, kgs)



    def metric_to_bmi(self, cm, kg):
        return str(kg / ((cm/100)**2))
        #print(self.ids.height_1.text)

    def convert_ft_to_cm(self, ft):
        return ft * 30.48

    def convert_inch_to_cm(self, inch):
        return inch * 2.54

    def convert_lbs_to_kg(self, lbs):
        return lbs / 2.205

    def imperial_to_bmi(self, ft, inch, lbs):
        kg = self.convert_lbs_to_kg(lbs)
        cm = self.convert_ft_to_cm(ft) + self.convert_inch_to_cm(inch)
        return self.metric_to_bmi(cm, kg)

    def imperial_button(self):
        self.height_1_bool = False
        self.height_units_1 = "ft"
        self.height_units_2 = "in"
        self.system = "imperial"
        self.weight_units = "lbs"

        #clean any value in the cm section
        self.ids.height_1.text = ""
        self.ids.height_2.text = ""
        self.ids.weight.text = ""

    def metric_button(self):
        self.height_1_bool = True
        self.height_units_1 = ""
        self.height_units_2 = "cm"
        self.system = "metric"
        self.weight_units = "kgs"

        #clean any value in the ft section
        self.ids.height_1.text = ""
        self.ids.height_2.text = ""
        self.ids.weight.text = ""

class NumericInput(MDTextField):
    max_characters = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(input_filter=self.char_limit, **kwargs)

    def on_focus(self, instance_text_field, focus_value: bool):
        # on focus request a numeric keyboard
        if focus_value:
            num_kb = Window.request_keyboard(self.close_key, self)
            if num_kb.widget:
                num_kb.widget.layout = 'numeric.json'

    def close_key(self):
        pass

    def char_limit(self, substring, from_undo):
        if len(self.text) < self.max_characters:
            return substring



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
