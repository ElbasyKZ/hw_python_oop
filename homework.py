class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения"""
        message = (f'Тип тренировки: {self.training_type};'
                   f' Длительность: {self.duration:.3f} ч.;'
                   f' Дистанция: {self.distance:.3f} км;'
                   f' Ср. скорость: {self.speed:.3f} км/ч;'
                   f' Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coef_callorie_1: int = 18
    coef_callorie_2: int = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_callories = ((self.coef_callorie_1 * self.get_mean_speed()
                           - self.coef_callorie_2) * self.weight
                           / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR))
        return spent_callories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_callories = ((0.035 * self.weight
                           + (self.get_mean_speed() ** 2 // self.height)
                           * 0.029 * self.weight) * self.duration
                           * self.MIN_IN_HOUR)
        return spent_callories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    swim_coef_1 = 1.1
    swim_coef_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_callories = ((self.get_mean_speed() + self.swim_coef_1)
                           * self.swim_coef_2 * self.weight)
        return spent_callories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_code[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    infomation = training.show_training_info()
    print(infomation.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
