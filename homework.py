from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type};'
                    ' Длительность: {duration:.3f} ч.;'
                    ' Дистанция: {distance:.3f} км;'
                    ' Ср. скорость: {speed:.3f} км/ч;'
                    ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    RUN_MS_MULTIPLIER: int = 18
    RUN_MS_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.RUN_MS_MULTIPLIER * self.get_mean_speed()
                + self.RUN_MS_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.HOUR_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_MS_MULTIPLIER: float = 0.035
    WLK_MS_SHIFT: float = 0.029
    KM_IN_M: float = 0.278
    SM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WLK_MS_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed()
                   * self.KM_IN_M)
                   ** 2
                   / (self.height
                      / self.SM_IN_M))
                * self.WLK_MS_SHIFT
                * self.weight)
                * (self.duration
                * self.HOUR_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_MS_MULTIPLIER: float = 1.1
    SWM_MS_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_MS_MULTIPLIER)
                * self.SWM_MS_SHIFT * self.weight
                * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in types:
        return types[workout_type](*data)
    return print('<Некорректный запрос>')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
