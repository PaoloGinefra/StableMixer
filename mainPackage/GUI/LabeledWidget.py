from .Addable import Addable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.graphics import Color
from .FitContentBoxLayout import FitContentBoxLayout


class LabeledWidget(Addable):
    def __init__(self, label: str, widget: Widget) -> None:
        super().__init__()
        self.layout = MDBoxLayout(orientation='horizontal')
        self.layout.size_hint = (1, None)
        self.label = MDLabel(text=label)
        self.label.size_hint = (None, None)
        self.label.halign = 'center'
        self.label.valign = 'center'
        self.layout.add_widget(self.label)

        widget.size_hint = (1, None)
        self.layout.add_widget(widget)

        # bind the height to the height of the widget
        self.layout.bind(height=widget.setter('height'))
        pass
