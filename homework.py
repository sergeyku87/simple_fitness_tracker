class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ):
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3} ч.; '
                f'Дистанция: {self.distance:.3} км; '
                f'Ср. скорость: {self.speed:.3} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = float(duration)
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    RATIO_SPEED: int = 18
    RATIO_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self):
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (
            (self.RATIO_SPEED * self.get_mean_speed()
             + self.RATIO_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATIO_HEIGHT_1: float = 0.035
    RATIO_HEIGHT_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self):
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self):
        """Получить среднюю скорость движения"""
        return super().get_mean_speed()

    def show_training_info(self):
        return super().show_training_info()

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        speed_m_on_sec = self.get_mean_speed() * (1 / 3.6)
        height_in_meter = self.height / 100
        time_in_min = self.duration * 60
        return (
            (self.RATIO_HEIGHT_1 * self.height
             + (speed_m_on_sec**2 / height_in_meter)
             * self.RATIO_HEIGHT_2 * self.height) * time_in_min)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

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

    def get_distance(self):
        """Получить дистанцию в км."""
        return super().get_distance()

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()

    def get_mean_speed(self):
        """Получить среднюю скорость плавания"""

        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        print(self.get_mean_speed(), 'speed')
        print(self.weight, 'weight')
        print(self.duration, 'time')
        return (
            (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
