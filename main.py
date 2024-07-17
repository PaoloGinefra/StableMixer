from mainPackage.Pipeline import Pipeline

from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons


def main():
    pipeline: Pipeline = Pipeline()
    pipeline.start()
    pass


if __name__ == "__main__":
    main()
