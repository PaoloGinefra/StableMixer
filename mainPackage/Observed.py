from .Observer import Observer


class Observed:
    def __init__(self) -> None:
        self.__observers = []

    def attach(self, observer: Observer) -> None:
        self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.__observers.remove(observer)

    def notify(self, volume: float) -> None:
        for observer in self.__observers:
            observer.update(volume)
