from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button


class FitContentBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super(FitContentBoxLayout, self).__init__(**kwargs)
        self._update_scheduled = False
        self.bind(children=self.schedule_update)

    def schedule_update(self, *args):
        if not self._update_scheduled:
            self._update_scheduled = True
            Clock.schedule_once(self.update_size, -1)

    def update_size(self, *args):
        self._update_scheduled = False

        # Calculate the width and height needed to fit the children
        if self.orientation == 'vertical':
            new_width = max(
                child.size_hint_x * self.width if child.size_hint_x else child.width for child in self.children)
            new_height = sum(
                child.size_hint_y * self.height if child.size_hint_y else child.height for child in self.children)
        else:
            new_width = sum(
                child.size_hint_x * self.width if child.size_hint_x else child.width for child in self.children)
            new_height = max(
                child.size_hint_y * self.height if child.size_hint_y else child.height for child in self.children)

        new_width += self.padding[0] + self.padding[2]
        new_height += self.padding[1] + self.padding[3]

        if self.size != (new_width, new_height):
            self.size = (new_width, new_height)
            self.minimum_size = (new_width, new_height)
            self.maximum_size = (new_width, new_height)
