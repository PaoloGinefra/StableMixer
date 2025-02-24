from kivy.uix.layout import Layout


class Addable():
    def __init__(self):
        self.layout: Layout = None
        pass

    def addThisTo(self, layout: Layout):
        layout.add_widget(self.layout)
