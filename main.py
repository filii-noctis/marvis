# Standard library imports
import os
import sys
from math import sin
from io import BytesIO

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

class MainScreen(Screen):
    """
    the default screen to show when the app is launched.
    """
    pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)  # passthrough constructor

    #     # UI layout
    #     layout = BoxLayout(orientation='vertical', spacing=0) # layout manager
    #     # TODD: add status bar to app

    #     # title/header div
    #     header_div = BoxLayout(
    #         orientation='vertical',
    #         size_hint_y=None, 
    #         height=dp(100), 
    #         padding=[ dp(15), dp(10) ])
        
    #     title = Label(text="Marvis", 
    #                   font_size=dp(22), 
    #                   color=(0.8, 0.8, 0.8, 1), 
    #                   bold=True, 
    #                   halign='left', 
    #                   size_hint_y=None, 
    #                   height=dp(30))

class MarvisApp(App):
    """
    Main app container
    contains build code and scaffolds the application
    view logic should ideally be abstracted outside this
    """
    def build(self):
        return MainScreen()
        # sm = ScreenManager()

        # home_screen = MainScreen(name='home')
        # sm.add_widget(home_screen)
        
        # sm.current = 'home'
        # return sm

if __name__ == '__main__':
    MarvisApp().run()
