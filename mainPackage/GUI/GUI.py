import threading
import time
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import matplotlib.pyplot as plt
import numpy as np
from kivy.clock import Clock
import seaborn as sns

from .LabeledWidget import LabeledWidget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..Pipeline import Pipeline


class GUI(MDApp):
    def __init__(self, pipeline: 'Pipeline') -> None:
        super().__init__()
        self.pipeline = pipeline

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        self.availableDevices = self.pipeline.getAvailableDevices()
        self.deviceMenu = DropDown()
        for device in self.availableDevices:
            btn = Button(text=device, size_hint_y=None, height=44)
            index = self.availableDevices.index(device)
            btn.bind(on_release=lambda btn: self.pipeline.setTargetDeciveIndex(
                index))
            self.deviceMenu.add_widget(btn)

        # deviceButton = Button(text='Select Device', size_hint=(1, 0.1))
        # deviceButton.bind(on_release=self.deviceMenu.open)
        # layout.add_widget(deviceButton)

        # def on_device_selected(instance, item):
        #     self.pipeline.setTargetDeciveIndex(
        #         self.availableDevices.index(item))
        # self.deviceMenu.bind(on_release=on_device_selected)

        self.runPIDCheckbox = MDCheckbox(
            active=True, size_hint=(1, 0.1))
        LabeledWidget("Run PID", self.runPIDCheckbox).addThisTo(layout)

        def on_checkbox_active(instance, value):
            self.pipeline.setPipelineRunning(value)

        self.runPIDCheckbox.bind(active=on_checkbox_active)

        self.slider = MDSlider(min=0, max=20, value=5,
                               step=0.1, size_hint=(1, 0.1))
        LabeledWidget("Target Volume", self.slider).addThisTo(layout)

        def on_slider_change(instance, value):
            self.pipeline.setTargetVolume(value)

        self.slider.bind(value=on_slider_change)

        # Set a Seaborn theme
        sns.set_theme(style='darkgrid')
        plt.tight_layout()
        self.fig, self.ax = plt.subplots()

        self.PcOutputVolumeLine, = self.ax.plot(
            self.pipeline.buffer.getBuffer(), label='PC Output Volume')
        # horizontal line
        self.targetVolumeLine, = self.ax.plot(
            [0, self.pipeline.buffer.size], [self.pipeline.getTargetVolume(), self.pipeline.getTargetVolume()], label='Target Volume')

        self.ax.legend()

        self.canvas = FigureCanvasKivyAgg(self.fig)
        layout.add_widget(self.canvas)

        # Schedule the plot to update at regular intervals
        Clock.schedule_interval(self.update_plot, 1.0 / 30.0)  # 30 FPS

        return layout

    def update_plot(self, dt):
        # Update the plot with the new buffer data
        self.PcOutputVolumeLine.set_ydata(self.pipeline.buffer.getBuffer())
        self.targetVolumeLine.set_ydata(
            [self.pipeline.getTargetVolume(), self.pipeline.getTargetVolume()])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw_idle()


if __name__ == '__main__':
    GUI().run()
