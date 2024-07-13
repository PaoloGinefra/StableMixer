from mainPackage.PcOutputHandler import PcOutputHandler
from mainPackage.PcOutputHandlerWindows import PcOutputHandlerWindows
from mainPackage.mainListener import MainListener

from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons


def main():
    mainListener: MainListener = MainListener()
    pcOutputHandler: PcOutputHandler = PcOutputHandlerWindows()

    targetVolumeSlider = Slider(plt.axes(
        [0.1, 0.01, 0.8, 0.03]), 'Target Volume', 0, 50, valinit=mainListener.targetVolume)

    runPIDCheck = CheckButtons(plt.axes(
        [0.1, 0.05, 0.1, 0.03]), ['Run PID'], [True])

    def update(val):
        mainListener.setTargetVolume(targetVolumeSlider.val)

    targetVolumeSlider.on_changed(update)

    def runPID(label):
        mainListener.runPID = not mainListener.runPID

    runPIDCheck.on_clicked(runPID)

    pcOutputHandler.addListener(mainListener)
    pcOutputHandler.run()
    pass


if __name__ == "__main__":
    main()
