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
from kivymd.uix.bottomsheet import MDListBottomSheet
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
from kivmob import KivMob, TestIds


class MainScreen(Screen):

    height_units_1 = StringProperty("ft")
    height_units_2 = StringProperty("in")
    height_1_bool = BooleanProperty(False)
    system = "imperial"
    current_text_button =  "height_1"
    weight_units = StringProperty('lbs')
    display_bmi = StringProperty("")
    display_font_size = NumericProperty("22")
    pointer_x = NumericProperty("0")
    movement = NumericProperty("0")
    steps = NumericProperty("0")
    movement_counter = 0
    step_increments = None
    clock_started = False
    display_bmi_category = StringProperty("")
    display_bmi_final = StringProperty("")

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        #place the red dot 10 meters out from the middle of the field
        pass

    def pass_fun(self):
        pass

    def show_ranges(self):
        #opens a bottom sheet
        bottom_sheet = MDListBottomSheet()
        bottom_sheet.bg_color = [107/255, 107/255, 107/255, 1]
        bottom_sheet.add_item('Below 18.5 --- Underweight', lambda x: self.pass_fun(), 'underweight_color.png')
        bottom_sheet.add_item('18.5 to 24.9 --- Healthy', lambda x: self.pass_fun(), 'healthy_color.png')
        bottom_sheet.add_item('25 to 29.9 --- Overweight', lambda x: self.pass_fun(), 'overweight_color.png')
        bottom_sheet.add_item('30 to 34.9 --- Obese Class 1', lambda x: self.pass_fun(), 'obese_color_1.png')
        bottom_sheet.add_item('35 to 39.9 --- Obese Class 2', lambda x: self.pass_fun(), 'obese_color_2.png')
        bottom_sheet.add_item('Over 40 --- Obese Class 3', lambda x: self.pass_fun(), 'obese_color_3.png')
        bottom_sheet.open()
    def check_final_bmi(self):
        # take the display bmi, see if it is too long and then return the value
        # to be displayed
        if float(self.display_bmi) > 100:
            # drop the decimal
            self.display_bmi_final = self.display_bmi.split('.')[0]
        else:
            self.display_bmi_final = self.display_bmi

        # if the display_bmi is more than 5 digits, shirnk the text size
        if float(self.display_bmi) > 99999:
            self.display_font_size = 15
        else:
            self.display_font_size = 22

        #if float(self.display_bmi) > 9999999:
        #    self.display_bmi = ""
        #    self.display_bmi_category = ""
        #else:
        #    self.display_font_size = 22

    def delete_text(self):
        if self.current_text_button == "height_1":
            # check if the string is empty
            if self.ids.height_1.text == "":
                # the there is nothing there, nothing to delete
                pass

            else:
                # there is a number there, get rid of the rightmost value
                self.ids.height_1.text = self.ids.height_1.text[:len(self.ids.height_1.text) - 1]



        if self.current_text_button == "height_2":
            # check if the string is empty
            if self.ids.height_2.text == "":
                # the there is nothing there, nothing to delete
                pass
            else:
                # there is a number there, get rid of the rightmost value
                self.ids.height_2.text = self.ids.height_2.text[:len(self.ids.height_2.text) - 1]

        if self.current_text_button == "weight":
            # check if the string is empty
            if self.ids.weight.text == "":
                # the there is nothing there, nothing to delete
                pass
            else:
                # there is a number there, get rid of the rightmost value
                self.ids.weight.text = self.ids.weight.text[:len(self.ids.weight.text) - 1]


    def set_downed_button_color(self):
        pass

    def bmi_ranges(self, bmi):
        if bmi == 0:
            return ""
        elif ((bmi > 0) & (bmi < 18.5)):
            return "Underweight"
        elif ((bmi >= 18.5) & (bmi < 25)):
            return "Healthy"
        elif ((bmi >= 25) & (bmi < 30)):
            return "Overweight"
        elif ((bmi >= 30) & (bmi < 35)):
            return "Obese Class 1"
        elif ((bmi >= 35) & (bmi < 40)):
            return "Obese Class 2"
        elif bmi >= 40:
            return "Obese Class 3"


    def height_1_button(self):
        self.current_text_button = "height_1"
        # when this is pressed it should clear, so reset the bmi category and display label
        # clear the display bmi and the bmi category
        self.display_bmi_final = ""
        self.display_bmi_category = ""

        if self.clock_started:

            self.pointer_x = 0
            self.clock_check.cancel()
            self.clock_started = False

        else:
            # the clock has not been started
            # but stil need to make sure that the pointer is
            # in the at zero
            self.pointer_x = 0


    def height_2_button(self):
        self.current_text_button = "height_2"
        # clear the display bmi and the bmi category
        self.display_bmi_final = ""
        self.display_bmi_category = ""

        if self.clock_started:

            self.pointer_x = 0
            self.clock_check.cancel()
            self.clock_started = False

        else:
            self.pointer_x = 0

    def weight_button(self):
        self.current_text_button = "weight"
        # clear the display bmi and the bmi category
        self.display_bmi_final = ""
        self.display_bmi_category = ""

        if self.clock_started:

            self.pointer_x = 0
            self.clock_check.cancel()
            self.clock_started = False

        else:
            self.pointer_x = 0

    def add(self, value):
        # takes a value from a button and then adds it to the text
        # of the correct button/label/text input
        if self.current_text_button == "height_1":

            # we don't want to have a decimal in here
            if value == '.':
                pass
            # check if the string is empty
            elif self.ids.height_1.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.height_1.text = str(value)

            else:
                # there is a number there, add the value to the right of that
                # but only if there is only one other number
                if len(self.ids.height_1.text) == 1:
                    self.ids.height_1.text = str(self.ids.height_1.text) + str(value)
                else: pass



        if self.current_text_button == "height_2":
            # check if the string is empty
            # we don't want to have a decimal in here

            if self.ids.height_2.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.height_2.text = str(value)
            else:
                # depending on what sytem we are using limit to 2 or 3 digits
                if self.system == 'Imperial':
                    # limit to 2
                    # there is a number there, add the value to the right of that
                    if len(self.ids.height_2.text) == 1:
                        self.ids.height_2.text = str(self.ids.height_2.text) + str(value)
                    else: pass
                else:
                    # limit to 3
                    # there is a number there, add the value to the right of that
                    if len(self.ids.height_2.text) <= 4:
                        self.ids.height_2.text = str(self.ids.height_2.text) + str(value)
                    else: pass


        if self.current_text_button == "weight":
            # check if the string is empty
            if self.ids.weight.text == "":
                # the there is nothing there, set value to be the new text
                self.ids.weight.text = str(value)
            else:
                # there is a number there, add the value to the right of that
                # limit to 5 digits, so there can be 3 with 1 decimal
                if len(self.ids.weight.text) <= 5:
                    self.ids.weight.text = str(self.ids.weight.text) + str(value)
                else:pass



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
                # clear the display bmi and the bmi category
                self.display_bmi_final = ""
                self.display_bmi_category = ""
                if self.clock_started:

                    self.pointer_x = 0
                    self.clock_check.cancel()
                    self.clock_started = False
                else:
                    self.pointer_x = 0

            else:
                # calculate the bmi
                # convert to floats
                # make sure that the lbs is not just a .
                if lbs == '.':
                    lbs = float(0)
                if inches == '.':
                    inches = float(0)

                ft = float(ft)
                inches = float(inches)
                lbs = float(lbs)
                self.display_bmi = self.imperial_to_bmi(ft, inches, lbs)
                self.check_final_bmi()
                self.display_bmi_category = self.bmi_ranges(float(self.display_bmi))
                self.pointer_position()

        else:
            # its not imperial so its the metric system
            cm = self.ids.height_2.text
            kgs = self.ids.weight.text

            if ((len(cm) == 0) | (len(kgs) == 0)):
                # we are missing some data
                # clear the display bmi and the bmi category
                self.display_bmi_final = ""
                self.display_bmi_category = ""
                if self.clock_started:

                    self.pointer_x = 0
                    self.clock_check.cancel()
                    self.clock_started = False

                else:
                    self.pointer_x = 0
            else:
                # we have everything we need
                # convert to floats

                if kgs == '.':
                    kgs = float(0)

                if cm == '.':
                    cm = float(0)

                cm = float(cm)
                kgs = float(kgs)
                self.display_bmi = self.metric_to_bmi(cm, kgs)
                self.check_final_bmi()
                self.display_bmi_category = self.bmi_ranges(float(self.display_bmi))
                self.pointer_position()

    def update(self, dt):
        # starts the clock and updates when the bmi is sucessfully caluclated
        time_factor = dt*60
        # so we have self.steps number of steps to move self.movement

        if self.movement < 0:
            speed = self.speed_piecewise(self.movement)
            self.pointer_x -= speed
            self.movement += speed

        elif ((self.movement > -.09) & (self.movement < .09)):
            # we are at the right spot stop the clock
            self.clock_check.cancel()
            self.clock_started = False


        else:
            speed = self.speed_piecewise(self.movement)
            self.pointer_x += speed
            self.movement -= speed

    def speed_piecewise(self, distance):
        distance = self.absolute_value(distance)

        if distance > 30:
            return 4
        elif distance <= 1:
            return .1
        else:
            return 1

    def absolute_value(self, x):
        if x < 0:
            return -x
        elif x >= 0:
            return x

    def calculate_steps(self):
        self.steps = 100
        # this many steps to get to the position
        self.step_increments = self.steps_function()

    def steps_function(self):
        # ok so we know that we are starting at self.pointer_x
        # we have to get to move self.movement pixels
        # and we have self.steps to get there.
        if self.movement > 0:
            gap = (self.movement - self.pointer_x) / self.steps
            x = []
            for i in range(self.steps):
                x.append(self.pointer_x + gap*i)
            return x
        if self.movement < 0:
            gap = (self.absolute_value(self.movement) - self.pointer_x) / self.steps
            x = []
            for i in range(self.steps):
                x.append(self.pointer_x + gap*i)

            return x






    def pointer_position(self):
        # need to get the current position of the pointer

        bmi_target = self.convert_bmi_to_pixels(self.display_bmi)
        # ok so this is the number of pixels that the pointer needs to get to

        # lets just round this to the tenth spot
        self.movement = round((bmi_target - self.pointer_x), 1)
        self.calculate_steps()

        self.movement_counter = 0

        # this is how the many pixels the pointer needs to move to get to the spot
        if self.clock_started == False:
            self.clock_check = Clock.schedule_interval(self.update, 1/60)
            self.clock_started = True


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
        if cm == 0:
            return str(0)
        else:
            return str(round( (kg / ((cm/100)**2)), 2 ))


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

        # clear the display bmi and the bmi category
        self.display_bmi_final = ""
        self.display_bmi_category = ""
        if self.clock_started:

            self.pointer_x = 0
            self.clock_check.cancel()
            self.clock_started = False

        else:
            self.pointer_x = 0

        if self.current_text_button == 'height_2':
            # so we are switching from cm to ft, the height 2 button has been selected
            # once the switch is made we will stay on this button
            self.ids.height_1.state = 'normal'

    def metric_button(self):
        # disable the height 1 button and the the background color to the base
        self.height_1_bool = True
        self.ids.height_1.background_disabled_normal = 'background.png'
        self.ids.height_1.state = 'normal'

        self.height_units_1 = ""
        self.height_units_2 = "cm"
        self.system = "metric"
        self.weight_units = "kgs"

        #clean any value in the ft section
        self.ids.height_1.text = ""
        self.ids.height_2.text = ""
        self.ids.weight.text = ""

        # clear the display bmi and the bmi category
        self.display_bmi_final = ""
        self.display_bmi_category = ""
        if self.clock_started:

            self.pointer_x = 0
            self.clock_check.cancel()
            self.clock_started = False

        else:
            self.pointer_x = 0

        # if the height_1 button has been selected, force switch to the height 2
        if self.current_text_button == 'height_1':
            self.current_text_button = 'height_2'
            self.ids.height_2.state = 'down'


class WindowManager(ScreenManager):
    pass

class BMICalculator(MDApp):

    def build(self):
        self.ads = KivMob(TestIds.APP) #put your ad id here
        self.ads.new_banner(TestIds.BANNER, top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()

    def on_start(self):
        if platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitch').alloc().init()

    def show_banner(self):
        self.banner_ad.show_ads()

    def hide_banner(self):
        self.banner_ad.hide_ads()



BMICalculator().run()
