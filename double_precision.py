#!/usr/bin/env python3
#!
# double_precision.py
# 
# Double Precision Modelling
#
# Written as part of a presentation on Glade Gtk.Builder and Gtk.Window.
# Incorporates conventional widget creation combined with Gtk.Builder creation.
# Includes base64 embedding of the logo / favicon image.
#
# Double precision specifications references:
# https://en.wikipedia.org/wiki/IEEE_754
# https://en.wikipedia.org/wiki/Double-precision_floating-point_format
# https://class.ece.iastate.edu/arun/Cpre305/ieee754/ie5.html
#
# Ian Stewart. May 2021.
#
import gi
gi.require_version('GdkPixbuf', '2.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
import time
import base64
import sys

# The following constants are used by the string variable 'glade_xml'.
AUTHOR = "Ian Stewart"
COMMENT = "Double Precision Modelling"
WEBSITE = "http://github.com/irsbugs/header-bar"
EMAIL = "stwrtn@gmail.com"

# General use constants
DATE = "2021-05-12"
TITLE = "Double Precision Modelling"
LABEL = "Modelling Double Precision / 64 Bit / IEEE754 Floating Point Data"

# DEBUG will display data to the console
DEBUG = False
# TESTING allows aspects of the Headerbar buttons to be functional.
TESTING = True


class Main_Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Menu Example")
        self.set_default_size(1100, 200)

        self.image = self.get_image_from_base64(B64_IMAGE) 
        # Add the Favicon
        self.set_icon(self.image)        
        
        # Path and filename of working file.
        self.filename = None
        self.main_data = "This is a test \n"

        # Use Builder to read embedded xml string defining HeaderBar
        self.builder = Gtk.Builder()
        self.builder.add_from_string(glade_xml)
        #self.builder.add_from_file("header_bar_4.glade")        
        self.header_bar = self.builder.get_object("headerbar")
        self.builder.connect_signals(self)
        self.set_titlebar(self.header_bar)

        self.header_bar.set_title(TITLE)
        self.header_bar.set_subtitle(DATE)

        # Now the Header Bar has been created insert the embedded image into it.
        image = self.builder.get_object("image_1")
        image.set_from_pixbuf(self.image)
                
        # Instantiate about dialog, which is hidden by default
        self.about = self.builder.get_object("about_dialog")
        # Add the logo image to the About dialog
        self.about.set_logo(self.image)
              
        
        # Add widgets using traditional method to the Gtk.Window
        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.label = Gtk.Label(label=LABEL)

        self.grid.attach(self.label, 0,0,1,1)
        self.add(self.grid)

        # Needs to be before the method to setup the mainframe
        self.main_frame_list = []
        self.main_label_bit_list = []
        self.main_frame_nibble_list = []
        self.main_frame_bit_list = []
        self.main_button_bit_list = []   

        # setup the frames in the display
        self.setup_64_bit_display_1()
        self.setup_sign_adjustment()
        self.setup_exponent_adjustment()
        self.setup_fraction_adjustment()
        self.setup_special_adjustment()       

        # Set initial value to +1.0
        for i in range(52,62):
            self.main_button_bit_list[0][i].set_label("1")
            
        self.update_frame_label()
        self.ieee754_breakdown()


    def setup_sign_adjustment(self):
        """ Toggling of the sign bit"""
        frame = Gtk.Frame(label="Sign")
        frame.set_label_align(0.1,0.5)
        frame.get_style_context().add_class("frame_main")        
        self.grid.attach(frame, 0,3,1,1)
        grid_adjust = Gtk.Grid()
        frame.add(grid_adjust)
        
        self.checkbutton_sign = Gtk.CheckButton(label="Unchecked positive / Checked negative")
        self.checkbutton_sign.connect("clicked", self.cb_sign_adjust)
        
        colour_label = Gtk.Label(label="   ")
        colour_label.get_style_context().add_class("label_key_colour")
        colour_label.get_style_context().add_class("colour_2")
        grid_adjust.attach(colour_label, 0,0,1,1)        
        
        grid_adjust.attach(self.checkbutton_sign, 1,0,1,1)
        
        
    def setup_exponent_adjustment(self):
        """Setup the exponent quick adjustments in a button box."""
        frame = Gtk.Frame(label="Exponent. Bias = 1023 ~ 3FF₁₆")
        frame.set_label_align(0.1,0.5)
        frame.get_style_context().add_class("frame_main")        
        self.grid.attach(frame, 0,4,1,1)
        grid_adjust = Gtk.Grid()
        frame.add(grid_adjust)
 
        colour_label = Gtk.Label(label="   ")
        colour_label.get_style_context().add_class("label_key_colour")
        colour_label.get_style_context().add_class("colour_1")
        grid_adjust.attach(colour_label, 0,0,1,1) 
 
        bbox = Gtk.ButtonBox()
        bbox.set_spacing(10)
        grid_adjust.attach(bbox, 1,0,1,1)
        
        button_list = ["1 ~ 3FF₁₆", "2 ~ 400₁₆", "Clear ~ 000₁₆", "All ~ 7FF₁₆"]       
        for item in button_list:
            button = Gtk.Button(label=item)
            button.connect("clicked", self.cb_button_exponent)        
            bbox.add(button)
    
    
    def setup_fraction_adjustment(self):
        """Setup the fraction quick adjustments in a button box."""
        frame = Gtk.Frame(label="Fraction")
        frame.set_label_align(0.1,0.5)
        frame.get_style_context().add_class("frame_main")        
        self.grid.attach(frame, 0,5,1,1)
        grid_adjust = Gtk.Grid()
        frame.add(grid_adjust)

        colour_label = Gtk.Label(label="   ")
        colour_label.get_style_context().add_class("label_key_colour")
        colour_label.get_style_context().add_class("colour_0")
        grid_adjust.attach(colour_label, 0,0,1,1)
 
        bbox = Gtk.ButtonBox()
        bbox.set_spacing(10)
        grid_adjust.attach(bbox, 1,0,1,1)
        
        button_list = [".000...", ".100...", ".000...", ".111...", ".0101...", ".1010..."]      
        for item in button_list:
            button = Gtk.Button(label=item)
            button.connect("clicked", self.cb_button_fraction)        
            bbox.add(button)

    def setup_special_adjustment(self):
        """Setup the special cases in a button box."""
        frame = Gtk.Frame(label="Special Cases")
        frame.set_label_align(0.1,0.5)
        frame.get_style_context().add_class("frame_main")        
        self.grid.attach(frame, 0,6,1,1)
        grid_adjust = Gtk.Grid()
        frame.add(grid_adjust)
 
        bbox = Gtk.ButtonBox()
        bbox.set_spacing(6)
        grid_adjust.attach(bbox, 0,0,1,1)
        
        button_list = ["+0", "-0", "+∞", "-∞", "+NaN", "-NaN", "Max +", "Max -", 
                "Min +", "Min -", "Max +64bit", "Max -64bit", "π" ]
                             
        for item in button_list:
            button = Gtk.Button(label=item)
            button.connect("clicked", self.cb_button_extreme)        
            bbox.add(button)        

    def cb_button_extreme(self, button):
        """Set the extreme limit floating point values"""
        
        if DEBUG: print("\nSpecial Cases button label:", button.get_label())         
        
        if button.get_label() == "+0":
            # 0 00000000000 0000000000000000000000000000000000000000000000000000 +0
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")        

        if button.get_label() == "-0":
            # 1 00000000000 0000000000000000000000000000000000000000000000000000 -0
            for i in range(0, 63):
                self.main_button_bit_list[0][i].set_label("0") 
            for i in range(63, 64):
                self.main_button_bit_list[0][i].set_label("1") 

        if button.get_label() == "+∞":
            # 0 11111111111 0000000000000000000000000000000000000000000000000000 +∞
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0") 
            for i in range(52, 63):
                self.main_button_bit_list[0][i].set_label("1") 

        if button.get_label() == "-∞":
            # 1 11111111111 0000000000000000000000000000000000000000000000000000 -∞
            for i in range(0, 53):
                self.main_button_bit_list[0][i].set_label("0") 
            for i in range(52, 64):
                self.main_button_bit_list[0][i].set_label("1")        
        
        if button.get_label() == "+NaN":
            # Nan - Can be anything in the fraction field ?
            # 0 11111111111 0000000000000000000000000000000000000000000000000001 +NaN
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0") 
            for i in range(52, 63):
                self.main_button_bit_list[0][i].set_label("1")
            for i in range(0, 1):
                self.main_button_bit_list[0][i].set_label("1")

        if button.get_label() == "-NaN":
            # Nan - Can be anything in the fraction field ?
            # 1 11111111111 0000000000000000000000000000000000000000000000000001 -NaN
            for i in range(0, 53):
                self.main_button_bit_list[0][i].set_label("0") 
            for i in range(52, 64):
                self.main_button_bit_list[0][i].set_label("1")
            for i in range(0, 1):
                self.main_button_bit_list[0][i].set_label("1")

        if button.get_label() == "Max +":
            # 1.7976931348623157 × 10**308
            # 0 11111111110 1111111111111111111111111111111111111111111111111111 Max +ve
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("1")
            self.main_button_bit_list[0][52].set_label("0")                           
            self.main_button_bit_list[0][63].set_label("0")           
            
        if button.get_label() == "Max -":
            # -1.7976931348623157 × 10**308
            # 1 11111111110 1111111111111111111111111111111111111111111111111111 Max -ve
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("1")
            self.main_button_bit_list[0][52].set_label("0")                           
 
        if button.get_label() == "Min +":  
            # 0 00000000001 0000000000000000000000000000000000000000000000000000 
            # ≙ 0010 0000 0000 000016 ≙ +2**−1022 × 1 ≈ 2.2250738585072014 × 10** −308 
            # (Min. normal positive double)
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")
            self.main_button_bit_list[0][52].set_label("1")  

        if button.get_label() == "Min -":  
            # 1 00000000001 0000000000000000000000000000000000000000000000000000 
            # ≙ 8010 0000 0000 0000 hex ≙ -2**−1022 × 1 ≈ -2.2250738585072014 × 10** −308 
            # (Min. normal positive double)
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")
            self.main_button_bit_list[0][52].set_label("1") 
            self.main_button_bit_list[0][63].set_label("1")  
        
        if button.get_label() == "Max +64bit":
            # 0 10000111110 0000000000000000000000000000000000000000000000000000 
            # 7FFF FFFF FFFF FFFF Maximum positive 64bit signed integer                              
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(53, 58):
                self.main_button_bit_list[0][i].set_label("1")             
            self.main_button_bit_list[0][62].set_label("1")             
            
        if button.get_label() == "Max -64bit":
            # 1 10000111110 0000000000000000000000000000000000000000000000000000
            # 8000 0000 0000 0000 Maximum negative 64bit signed integer        
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(53, 58):
                self.main_button_bit_list[0][i].set_label("1")                            
            for i in range(62, 64):
                self.main_button_bit_list[0][i].set_label("1")

            
        if button.get_label() ==  "π":
            # 0 10000000000 1001001000011111101101010100010001000010110100011000 
            # 4009 21FB 5444 2D1816 ≈ pi
            s = "1001001000011111101101010100010001000010110100011000"
            s = s[::-1]
            for i in range(0, 64):
                self.main_button_bit_list[0][i].set_label("0")           
            self.main_button_bit_list[0][62].set_label("1")           
            for i in range(len(s)):
                self.main_button_bit_list[0][i].set_label(s[i:i+1]) 
            
            
        self.update_frame_label()
        self.ieee754_breakdown()  

    def cb_button_fraction(self, button):
        """
        Set exponent bits and then update
        button_list = [".000...", ".100...", ".000...", ".111...", ".0101...", ".1010..."]
        """
        if DEBUG: print("\nExponent button label:", button.get_label())

        if button.get_label() == ".000...":
            for i in range(0, 52):
                self.main_button_bit_list[0][i].set_label("0")

        if button.get_label() == ".100...":
            for i in range(0, 51):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(51,52):
                 self.main_button_bit_list[0][i].set_label("1")         

        if button.get_label() == ".000...":
            for i in range(0, 52):
                self.main_button_bit_list[0][i].set_label("0")

        if button.get_label() == ".111...":
            for i in range(0, 52):
                self.main_button_bit_list[0][i].set_label("1")
                                
        if button.get_label() == ".0101...":
            for i in range(0, 52):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(0, 52, 2):
                self.main_button_bit_list[0][i].set_label("1")                               

        if button.get_label() == ".1010...":
            for i in range(0, 52):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(1, 52, 2):
                self.main_button_bit_list[0][i].set_label("1") 

        self.update_frame_label()
        self.ieee754_breakdown()                
                        
        
    def cb_button_exponent(self, button):
        """
        Set exponent bits and then update
        ["1 ~ 3FF₁₆", "2 ~ 400₁₆", "Clear ~ 000₁₆", "All ~ 7FF₁₆"]  
        """
        if DEBUG: print("\nExponent button label:", button.get_label())
        
        if button.get_label() == "1 ~ 3FF₁₆":
            for i in range(52,62):
                self.main_button_bit_list[0][i].set_label("1")
            for i in range(62,63):
                 self.main_button_bit_list[0][i].set_label("0")               

        if button.get_label() == "2 ~ 400₁₆":
            for i in range(52,62):
                self.main_button_bit_list[0][i].set_label("0")
            for i in range(62,63):
                 self.main_button_bit_list[0][i].set_label("1")  

        if button.get_label() == "Clear ~ 000₁₆":
            for i in range(52,63):
                self.main_button_bit_list[0][i].set_label("0")
  
        if button.get_label() == "All ~ 7FF₁₆":
            for i in range(52,63):
                self.main_button_bit_list[0][i].set_label("1")
                
        self.update_frame_label()
        self.ieee754_breakdown()        
    
    
    def cb_sign_adjust(self, check_button):
        if DEBUG: print("\nSign button:", check_button.get_active())
        if check_button.get_active():
            self.main_button_bit_list[0][63].set_label("1")
        else:
            self.main_button_bit_list[0][63].set_label("0")   
        self.update_frame_label()
        self.ieee754_breakdown()


    def ieee754_breakdown(self, index = 0):
        """Display a breakdown of an IEEE 754"""
        bias = 1023
        
        # Sign bit       
        sign = int(self.main_button_bit_list[index][63].get_label())
        if DEBUG: print("Sign:", sign)
        
        # Exponent
        s = ""
        for i in range(52, 63):
            s += self.main_button_bit_list[index][i].get_label()
        s = s[::-1]
        if DEBUG: print("Exponent in binary:", s)
        exponent = int(s,2) - bias
        if DEBUG: print("Exponent:", exponent)

        # Mantissa
        s = ""
        for i in range(0, 52):
            s += self.main_button_bit_list[index][i].get_label()
        s = s[::-1]
        if DEBUG: print(s)  # left to right 0 to 2**-52               
        fraction = 0 
        for idx, value in enumerate(s):
            #print(index, value)
            fraction += int(value) * 2**-(idx + 1)
        if DEBUG: print("fraction:", fraction)

        # Calculation...
        # (-1)**sign bit * (1+fraction) * 2 ** exponent - bias
        # Sing bit: (-1)**0 = 1, (-1)**1 = -1 

        try:
            if fraction == 0 and exponent == -1023 and sign == 0:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: +0.0")                
            elif fraction == 0 and exponent == -1023 and sign == 1:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: -0.0")
                    
            elif fraction == 0 and exponent == 1024 and sign == 0:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: +∞")                       

            elif fraction == 0 and exponent == 1024 and sign == 1:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: -∞") 

            # NaN seems to be anything in the fraction if exponent is 1024.
            elif fraction > 0 and exponent == 1024 and sign == 0:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: +NaN") 
                    
            elif fraction > 0 and exponent == 1024 and sign == 1:
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: -NaN") 


            else:
                # Perform the calculation of the floating point value
                decimal_value = (-1)**sign * (1 + fraction) * (2**exponent)
                if DEBUG: print("decimal_value:", decimal_value)
                if DEBUG: print(self.main_frame_list[index].get_label())
                self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                        " ~ Floating Point: " + str(decimal_value)) 
                
                # Append a message after providing the fp value
                # If Max +ve or Max -ve append to label        
                if fraction > 0 and exponent == 1023 and sign == 0:
                    self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                            " ~ Max +ve ")        
                            
                # If Max +ve or Max -ve append to label        
                if fraction > 0 and exponent == 1023 and sign == 1:
                    self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                            " ~ Max -ve ")                              
                
                # Min + - Closest to zero?                     
                # 0 00000000001 0000000000000000000000000000000000000000000000000000 
                if fraction == 0 and exponent == -1022 and sign == 0:
                    self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                            " ~ Min +ve")                                                 

                if fraction == 0 and exponent == -1022 and sign == 1:
                    self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                            " ~ Min -ve")                                        
                        
        except OverflowError:
            print("WARNING: OverflowError: int too large to convert to float") 
            self.main_frame_list[index].set_label(self.main_frame_list[index].get_label() + 
                    " ~ Floating Point: Overflow Error" )

        # Sync up the checkbutton with bit 63
        if self.main_button_bit_list[0][63].get_label() == "0":
            self.checkbutton_sign.set_active(False)
        else:
            self.checkbutton_sign.set_active(True)   
                     
        
    def update_frame_label(self):
        """
        Convert the 4 x bit nibble to hex for nibble frame label.
        Place all the nibble labels in the main frame label.
        Updates all main frames
        """
        count = len(self.main_frame_list)

        for idx in range(count):  #Start, count)                  
            s1 = ""
            for i in range(16): #self.main_frame_nibble_list:  # 16
                s = ""
                for j in range(4):
                    s += str(self.main_button_bit_list[idx][i*4 + j].get_label())
                s = s[::-1]
                self.main_frame_nibble_list[idx][i].set_label(str(hex(int(s,2)))[2:].upper())
                s1 += str(self.main_frame_nibble_list[idx][i].get_label())
            s1 = s1[::-1]
            if DEBUG: print("\n" + s1[:8] + " " + s1[8:])
            self.main_frame_list[idx].set_label(s1[:8] + " " + s1[8:])            


    def setup_64_bit_display_1(self):
        """
        A 64 bit binary display. 
        2 x rows of 32 x labels in frames. Frame buttons give the bit number.
        i = 2 rows, j = 8 nibbles per row, k = 4 bits per nibble. total = 64 bits
        Contained in self.main_frame attached to the Window grid
        self required for button_bit_list, frame_bit_list, frame_nibble_list, main_frame.
        """
        main_frame = Gtk.Frame(label="Main Frame 0")
        main_frame.set_label_align(0.1,0.5)
        main_frame.get_style_context().add_class("frame_main")
        
        self.main_frame_list.append(main_frame)
        
        # Increment placement on window grid based on length of mainframe
        position = len(self.main_frame_list)
        self.grid.attach(self.main_frame_list[-1], 0,position,1,1)       
        
        # Grid_frame. Grid for the 16 x nibble frames
        grid_frame = Gtk.Grid()
        self.main_frame_list[-1].add(grid_frame) 
        
        # Temp lists. These get wiped out. Only good for the current pass       
        frame_nibble_list = []
        grid_nibble_list = []
        frame_bit_list = []        
        button_bit_list = []
        s = ""
        
        for i in range(2):  # rows 2**5 = 32
            # i is reserved for producing two rows
            for j in range(8):  # nibbles per row 2**2 = 4
                # Create the 16 nibble frames and place in frame_nibble_list
                frame_nibble = Gtk.Frame(label=str(i*8+j).zfill(2))
                frame_nibble.get_style_context().add_class("frame_nibble")
                frame_nibble.set_label_align(0.5,0.5)
                frame_nibble_list.append(frame_nibble)

                # Place a grid in each of the 16 nibble frame
                grid_nibble = Gtk.Grid()
                grid_nibble_list.append(grid_nibble)
                frame_nibble_list[i*8+j].add(grid_nibble_list[i*8+j])

                # Attach the nibble frames (and their nibble grids) into the grid frame.
                # Two rows, bottom 0 to 7 and top 8 to 15                                
                if i*8+j < 8:
                    grid_frame.attach(frame_nibble_list[i*8+j], 8-j,1,1,1)
                else:
                    grid_frame.attach(frame_nibble_list[i*8+j], 8-j,0,1,1)               
            
                for k in range(4):  # bit per frame i*32+j*4+k
                    #Create the 4 bit frames to insert into grid_nibbles in each frame_nibble
                    frame_bit = Gtk.Frame(label=str(i*32+j*4+k).zfill(2))
                    #print(i*32+j*4+k)
                    frame_bit.get_style_context().add_class("frame_bit")
                    frame_bit.set_label_align(0.5,0.5)
                    
                    # Add the IEEE 754 colouring for sign, exponent and fraction.
                    if i*32+j*4+k <= 51:
                        frame_bit.get_style_context().add_class("colour_0")
                    elif i*32+j*4+k >= 52 and i*32+j*4+k <= 62:
                        frame_bit.get_style_context().add_class("colour_1")                        
                    else:
                        frame_bit.get_style_context().add_class("colour_2")
                
                    # Button bits. Add into each frame bit. Label set to 0.
                    button_bit = Gtk.Button(label="0")
                    button_bit.get_style_context().add_class("button_bit")
                    button_bit.connect("clicked", self.cb_button_bit, i*32+j*4+k)                     
                    button_bit_list.append(button_bit)
                    
                    # Add the button bits to their frames
                    frame_bit.add(button_bit_list[i*32+j*4+k]) 
                    frame_bit_list.append(frame_bit)                    
                    
                    # Bottom row 0 to 31 and top row 32 to 63
                    if not i:    
                        grid_nibble_list[i*8+j].attach(frame_bit_list[i*32+j*4+k], 
                                                        32-i*32+j*4-k,1,1,1)
                    else:
                        grid_nibble_list[i*8+j].attach(frame_bit_list[i*32+j*4+k], 
                                                        64-i*32+j*4-k,0,1,1)                

        # Permanent lists. Plus, self.main_frame_list
        self.main_button_bit_list.append(button_bit_list)        
        self.main_frame_nibble_list.append(frame_nibble_list)
        self.main_frame_bit_list.append(frame_bit_list)

 
    def cb_button_bit(self, button, ident):
        """Toggle the button bit. Ident is integer from 0 to 63"""
        if DEBUG: print("Buttons Bit Identity:", ident)
        # Toggle 0 to 1 and 1 to 0. if a=0, a = abs(a-1), then a=1
        button.set_label(str(abs(int(button.get_label())-1)))
        self.update_frame_label()
        self.ieee754_breakdown()
        
        
    # Callbacks on Main buttons in header bar
    def cb_open(self, button):
        """Open button on Header Bar. Sets self.filename variable"""
        print("Open File callback")
        dialog = Gtk.FileChooserDialog(
                title="Please choose a file", 
                parent=self, 
                action=Gtk.FileChooserAction.OPEN
                )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
                )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.filename = dialog.get_filename()
            if TESTING:
                # Testing. Place a time stamp into the file each time it is opened.
                # E.g. 'Fri May  7 16:46:41 2021'
                with open(self.filename, "a") as fout:
                    fout.write("Opened: " + time.ctime() + "\n")            
                
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
        
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)  


    def cb_new(self, button):
        """Select a new file"""
        print("New File callback")
        self.cb_save_as(button)
        

    def cb_save(self, button):
        """Save button on Header Bar. Save unless variable not set."""
        print("Save File callback")

        if self.filename:
            with open(self.filename, "w") as fout:
                fout.write(self.main_data)
        else:
            # If self.flename is blank then call the Save_As method.
            self.cb_save_as(button)
        
        
    def cb_save_as(self, button):
        """Save_as button on Header Bar. Opens Dialog, sets variable, and saves"""
        print("Save_As File callback")        
        dialog = Gtk.FileChooserDialog(
                title="Please provide a file name", 
                parent=self, 
                action=Gtk.FileChooserAction.SAVE
                )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
                )

        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Save button clicked")
            print("File selected: " + dialog.get_filename())
            self.filename = dialog.get_filename()

            # Write main data to file
            with open(self.filename, "w") as fout:
                fout.write(self.main_data)            
                        
            if TESTING:
                # Testing. Place a time stamp into the file each time it is opened.
                # E.g. 'Fri May  7 16:46:41 2021'
                with open(self.filename, "a") as fout:
                    fout.write("Created: " + time.ctime() + "\n")             
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


    # Callbacks for Popover main menu
    def cb_close(self, *args):
        """ Main close in Popover menu"""
        Gtk.main_quit()    
    
    
    def cb_something_1(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 1")  


    def cb_something_2(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 2")  


    def cb_something_3(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 3")  


    def cb_something_4(self, button):
        """Modify to meet the needs of the application."""        
        print("Do Something 4")  
     
       
    def cb_about_show(self, button):
        """Show the About dialog."""        
        print("About Dialog show")  
        self.about_dialog = self.builder.get_object("about_dialog")  
        self.about_dialog.show_all()
               
    # Callback in About Dialog           
    def cb_about_hide(self, *args):
        """About dialog. Response to Close button.""" 
        print("About Dialog hide")
        self.about_dialog.hide()


    def get_image_from_base64(self, b64_image):
        '''
        B64_IMAGE is decoded it to binary bytes.
        Load the bytes using GdkPixbuf.PixbufLoader
        Return the Pixbuf image.
        '''
        # Decode base64 data
        image_data = base64.decodebytes(b64_image)
        
        # Use PixbufLoader to load the image_data to Pixbuf data.
        loader = GdkPixbuf.PixbufLoader()        
        loader.write(image_data)
        loader.close()
        pixbuf = loader.get_pixbuf()                 
        return pixbuf 


def add_provider(widget):
    # Provide the CSS for labels and frames.
    screen = widget.get_screen()
    style = widget.get_style_context()
    provider = Gtk.CssProvider()
    provider.load_from_data("""
    .label_bit {
        margin: 10px;
        font: 20px Arial, sans-serif;
        }

    .label_key_colour {
        border: 1px solid #000000;
        margin-left: 15px;
        margin-right: 15px;        
        margin-bottom: 5px;
        font: 16px Arial, sans-serif;
        }   
        
    .label_key_description {
        margin-left: 2px;
        margin-bottom: 5px;
        font: 16px Arial, sans-serif;
        }         

    .button_bit {
        margin: 2px;
        font: 20px Arial, sans-serif;
        color: #FF0000;
        }

             
    .frame_bit {
        margin: 2px;
        font: 12px Courier New, monospace;
        } 
    
    .frame_nibble {
        margin: 2px;
        font: 20px Arial, sans-serif;
        }     
    
    .frame_main {
        /* border: 1px solid #000000; */
        margin: 5px;
        font: 20px Arial, sans-serif;
        }
        
    .frame_category {
        margin: 2px;
        font: 20px Arial, sans-serif;
        }        

    .frame_register {
        margin: 2px;
        font: 20px Arial, sans-serif;
        }        

    .frame_register_list {
        /* margin-left: 10px;
        margin-right: 5px;
        margin-bottom: 5px; */
        margin: 5px;
        font: 16px Courier New, monospace;
        /* Arial, sans-serif;*/
        } 

    .treeview_category {
        margin: 2px;
        font: 16px Arial, sans-serif;
        } 

    .button_category {
        /* margin-left: 10px;
        margin-right: 5px;
        margin-bottom: 5px; */
        margin: 5px;
        font: 16px Arial, sans-serif;
        } 
                
    .radio_category {
        margin-left: 10px;
        margin-right: 5px;
        margin-bottom: 5px;
        font: 16px Arial, sans-serif;
        }    

    .colour_0 {
        background: Aquamarine;
        /*background: rgb(255,160,160)*/
        }
    
    .colour_1 {
        background: MistyRose;
        }     

    .colour_2 {
        background: PaleGreen;
        }
 
    .colour_3 {
        background: Khaki;
        }  
    """.encode('utf-8')) 
     
    style.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

# Image used as the logo.
B64_IMAGE = (b"""
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
""")


"""
In the following glade_xml, format substitution is used for name as {0}, 
comment as {1}, website {2}, email{3}. i.e. .format(AUTHOR, COMMENT, WEBSITE, EMAIL, LOGO)
E.g. 

    <property name="copyright" translatable="yes">© 2021 {0}.</property>
    <property name="comments" translatable="yes">{1}</property>
    <property name="website">{2}</property>
    <property name="website-label" translatable="yes">Source Code web site</property>
    <property name="authors">{0} &lt;{3}&gt;
    <property name="logo">{4}</property>
"""

glade_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.38.1 

Glade - A user interface designer for GTK+ and GNOME.
Copyright (C) 2012-2018 Juan Pablo Ugarte

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Author: Juan Pablo Ugarte

-->
<interface domain="glade">
  <requires lib="gtk+" version="3.20"/>
  <!-- interface-license-type lgplv2 -->
  <!-- interface-name Glade -->
  <!-- interface-description A user interface designer for GTK+ and GNOME. -->
  <!-- interface-copyright 2012-2018 Juan Pablo Ugarte -->
  <!-- interface-authors Juan Pablo Ugarte -->
  <object class="GtkAboutDialog" id="about_dialog">
    <property name="can-focus">False</property>
    <property name="border-width">5</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="type-hint">dialog</property>
    <property name="copyright" translatable="yes">© 2021 {0}.</property>
    <property name="comments" translatable="yes">{1}</property>
    <property name="website">{2}</property>
    <property name="website-label" translatable="yes">Source Code web site</property>
    <property name="authors">{0} &lt;{3}&gt;</property>
    <!-- property name="logo"></property -->
    <property name="license-type">gpl-3-0</property>
    <signal name="response" handler="cb_about_hide" swapped="no"/>
    <child internal-child="vbox">
      <object class="GtkBox" id="aboutdialog-vbox1">
        <property name="can-focus">False</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="aboutdialog-action_area1">
            <property name="can-focus">False</property>
            <property name="layout-style">end</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="pack-type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkPopoverMenu" id="main_menu">
    <property name="can-focus">False</property>
    <child>
      <object class="GtkBox">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="border-width">4</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Close Project</property>
            <signal name="clicked" handler="cb_close" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 1</property>
            <signal name="clicked" handler="cb_something_1" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 2</property>
            <signal name="clicked" handler="cb_something_2" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 3</property>
            <signal name="clicked" handler="cb_something_3" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">4</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 4</property>
            <signal name="clicked" handler="cb_something_4" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">5</property>
          </packing>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">6</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">About</property>
            <signal name="clicked" handler="cb_about_show" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">7</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="submenu">main</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
  <object class="GtkHeaderBar" id="headerbar">
    <property name="name">headerbar</property>
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="show-close-button">True</property>
    <child>
      <object class="GtkImage" id="image_1">
        <property name="name">image_1</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
      </object>                   
      <packing>
        <property name="pack-type">start</property>      
        <property name="position">0</property>
      </packing>
    </child>     
    <child>
      <object class="GtkMenuButton">
        <property name="name">menu-button</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
        <property name="tooltip-text" translatable="yes">Main Menu</property>
        <property name="popover">main_menu</property>
        <child>
          <object class="GtkImage">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="icon-name">open-menu-symbolic</property>
          </object>
        </child>
      </object>
      <packing>
        <property name="pack-type">end</property>
        <property name="position">1</property>
      </packing>
    </child>
    <child>
      <object class="GtkButtonBox" id="open_button_box">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="layout-style">expand</property>
        <child>
          <object class="GtkButton">
            <property name="label" translatable="yes">_Open</property>
            <property name="name">open-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Open a project</property>
            <property name="use-underline">True</property>
            <property name="always-show-image">True</property>
            <signal name="clicked" handler="cb_open" swapped="no"/>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
            <property name="non-homogeneous">True</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="position">1</property>
      </packing>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkButton">
        <property name="name">new-button</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
        <property name="tooltip-text" translatable="yes">Create a new file</property>
        <signal name="clicked" handler="cb_new" swapped="no"/>
        <child>
          <object class="GtkImage">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="icon-name">document-new-symbolic</property>
          </object>
        </child>
      </object>
      <packing>
        <property name="position">2</property>
      </packing>
    </child>
    <child>
      <object class="GtkButtonBox" id="save_button_box">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="layout-style">expand</property>
        <child>
          <object class="GtkButton">
            <property name="label" translatable="yes">_Save</property>
            <property name="name">save-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Save the current project</property>
            <property name="use-underline">True</property>
            <signal name="clicked" handler="cb_save" swapped="no"/>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton">
            <property name="name">save-as-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Save the current project with a different name</property>
            <property name="use-underline">True</property>
            <signal name="clicked" handler="cb_save_as" swapped="no"/>
            <child>
              <object class="GtkImage">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="icon-name">document-save-as-symbolic</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="pack-type">end</property>
        <property name="position">3</property>
      </packing>
    </child>
    <child>
      <placeholder/>
    </child>
  </object>
</interface>
""".format(AUTHOR, COMMENT, WEBSITE, EMAIL)

win = Main_Window()
win.connect("realize", add_provider)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

"""
# Notes:
# Exponents range from −1022 to +1023 
# because exponents of −1023 (all 0s) and +1024 (all 1s) are reserved 
# for special numbers. 3ff = 1023 7fe = 2046
# Bias = 1023
# +2**1023  11111111110 7FE Max positive
# +2**−1022 00000000001 001 Max negative
#           10000000000 400 = 2
#           01111111111 3FF = 1
# (-1)**sign  x  2 **(exponent - 1023)  x  1.fraction
# 00000000000 = 000 hex is used to represent a signed zero (if F = 0) 
# and subnormals (if F ≠ 0);
# 11111111111 = 7ff hex is used to represent ∞ (if F = 0) and NaNs (if F ≠ 0),
"""
