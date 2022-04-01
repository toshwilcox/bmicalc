from kivy.config import Config
Config.set('graphics', 'width', 360 )
Config.set('graphics', 'height', 600)
#Config.set("kivy", "keyboard_mode", 'dock')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
#import numpy as np
import math
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.textinput import TextInput


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
from kivy.utils import platform
from kivy.properties import Clock

class MainScreen(Screen):

    height_units_1 = StringProperty("ft")
    height_units_2 = StringProperty("in")
    height_1_bool = BooleanProperty(False)
    system = "imperial"
    current_text_button =  "height_1"
    weight_units = StringProperty('lbs')
    display_bmi = StringProperty("")
    pointer_x = NumericProperty("0")
    movement = NumericProperty("0")

    def height_1_button(self):
        self.current_text_button = "height_1"

    def height_2_button(self):
        self.current_text_button = "height_2"

    def weight_button(self):
        self.current_text_button = "weight"

    def add(self, value):
        # takes a value from a button and then adds it to the text
        # of the correct button/label/text input
        if self.current_text_button == "height_1":
            # check if the string is empty
            if self.ids.height_1.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.height_1.text = str(value)

            else:
                # there is a number there, add the value to the right of that
                self.ids.height_1.text = str(self.ids.height_1.text) + str(value)



        if self.current_text_button == "height_2":
            # check if the string is empty
            if self.ids.height_2.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.height_2.text = str(value)
            else:
                # there is a number there, add the value to the right of that
                self.ids.height_2.text = str(self.ids.height_2.text) + str(value)


        if self.current_text_button == "weight":
            # check if the string is empty
            if self.ids.weight.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.weight.text = str(value)
            else:
                # there is a number there, add the value to the right of that
                self.ids.weight.text = str(self.ids.weight.text) + str(value)



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
                #Clock.schedule_interval(self.update, 1/60)
                self.pointer_position()

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
                #Clock.schedule_interval(self.update, 1/60)
                self.pointer_position()

    def update(self, dt):
        # starts the clock and updates when the bmi is sucessfully caluclated
        time_factor = dt*60

        if self.movement < 0:
            self.pointer_x -= time_factor
            self.movement += time_factor

        else:
            self.pointer_x += time_factor
            self.movement -= time_factor

    def pointer_position(self):
        # need to get the current position of the pointer

        bmi_target = self.convert_bmi_to_pixels(self.display_bmi)
        # ok so this is the number of pixels that the pointer needs to get to

        self.movement = bmi_target - self.pointer_x
        print(self.movement)
        # this is how the many pixels the pointer needs to move to get to the spot
        Clock.schedule_interval(self.update, 1/60)


    def convert_bmi_to_pixels(self, bmi):

        if float(bmi) < 14:
            bmi = float(14)
        elif float(bmi) > float(44):
            bmi = float(44)
        width = Window.size[0]
        # there is a 10% padding on the left hand side
        padding = width * .1

        # the range goes from 14 - 44
        # which is 80% of the screen width

        meter_size = width*.8

        # the scale starts at 14 and is 30 units long
        # this will get what percentage of the scale we are on.
        bmi_pixel = meter_size  * (float(bmi) - 14) / 30

        return bmi_pixel




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
        print('poop')
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
            print(self.close_key)
            num_kb = Window.request_keyboard(self.close_key, self)
            print(num_kb.widget)
            if num_kb.widget:
                print('yes')
                num_kb.widget.layout = 'numeric.json'

    def close_key(self):
        pass

    def char_limit(self, substring, from_undo):
        if len(self.text) < self.max_characters:
            return substring


class CustomTextField(MDTextField):
    def __init__(self, *args, **kwargs):
        self.input_type = "number"
        self.input_type = "tel"
        self.input_filter = 'float'
        self.multiline = False
        super().__init__(**kwargs)



class WindowManager(ScreenManager):
    pass

class BMICalculator(MDApp):

    def build(self):
        pass

    def on_start(self):
        print('start')
        if platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitch').alloc().init()

    def show_banner(self):
        self.banner_ad.show_ads()

    def hide_banner(self):
        self.banner_ad.hide_ads()



BMICalculator().run()
