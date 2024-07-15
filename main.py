from mainPackage.Pipeline import Pipeline

from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons


def main():
    pipeline: Pipeline = Pipeline()
    print(pipeline.getAvailableDevices())

    targetVolumeSlider = Slider(plt.axes(
        [0.1, 0.01, 0.8, 0.03]), 'Target Volume', 0, 50, valinit=pipeline.getTargetVolume())

    runPIDCheck = CheckButtons(plt.axes(
        [0.1, 0.05, 0.1, 0.03]), ['Run PID'], [True])

    def update(val):
        pipeline.setTargetVolume(targetVolumeSlider.val)

    targetVolumeSlider.on_changed(update)

    def runPID(label):
        pipeline.setPipelineRunning(not pipeline.isRunning())

    runPIDCheck.on_clicked(runPID)

    pipeline.start()
    pass


if __name__ == "__main__":
    main()
