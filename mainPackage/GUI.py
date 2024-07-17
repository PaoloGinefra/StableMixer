import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.clock import Clock
import seaborn as sns

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Pipeline import Pipeline


class GUI(App):
    def __init__(self, pipeline: 'Pipeline') -> None:
        super().__init__()
        self.pipeline = pipeline

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10,
                           spacing=10)

        self.runPIDCheckbox = CheckBox(
            active=True, size_hint=(1, 0.1))
        layout.add_widget(self.runPIDCheckbox)

        def on_checkbox_active(instance, value):
            self.pipeline.setPipelineRunning(value)

        self.runPIDCheckbox.bind(active=on_checkbox_active)

        self.slider = Slider(min=0, max=20, value=5,
                             step=0.1, size_hint=(1, 0.1))
        layout.add_widget(self.slider)

        def on_slider_change(instance, value):
            self.pipeline.setTargetVolume(value)

        self.slider.bind(value=on_slider_change)

        # Set a Seaborn theme
        sns.set_theme(style='darkgrid')

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
