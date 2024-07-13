import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.clock import Clock
import seaborn as sns


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.button = Button(text='Click Me')
        layout.add_widget(self.button)

        # Set a Seaborn theme
        sns.set_theme(style='darkgrid')

        self.fig, self.ax = plt.subplots()
        self.x_data = np.linspace(0, 10, 100)
        self.line, = self.ax.plot(self.x_data, np.sin(self.x_data))

        self.canvas = FigureCanvasKivyAgg(self.fig)
        layout.add_widget(self.canvas)

        # Start the animation thread
        self.animation_thread = threading.Thread(target=self.run_animation)
        self.animation_thread.daemon = True
        self.animation_thread.start()

        return layout

    def update_plot(self, dt):
        self.line.set_ydata(np.sin(self.x_data + Clock.get_time()))
        self.canvas.draw_idle()

    def run_animation(self):
        while True:
            # Use Clock.schedule_once to update the plot safely from another thread
            Clock.schedule_once(self.update_plot, 0)
            time.sleep(1 / 30)  # Sleep to achieve 30 updates per second


if __name__ == '__main__':
    MyApp().run()
