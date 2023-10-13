from dataclasses import asdict, dataclass
from typing import ClassVar, Union


@dataclass
class InfoMessage:
    """
    A class for storing and displaying information.

    ...

    Attributes
    ----------
    training_type: str
        type of training conducted
    duration: float
        time spent training
    distance: float
        distance covered during training
    speed: float
        average speed during training
    calories: float
        number of calories spent

    TYPE: str
        line for displaying the type of training
    TIME: str
        line for displaying the training time spent
    DIST: str
        line for displaying of the distance covered
    SPEED: str
        line for displaying the speed of movement
    CALORIES: str
        line for displaying of calories spent

    Methods
    -------
    get_message()
        displays information about the training

    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Displays a message about the training session."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """
    Base class for description training.


    ...

    Attributes
    ----------
    LEN_STEP: float
        average step length
    M_IN_KM: int
        number of meters per kilometer
    MIN_IN_HR
        number of minutes per hour
    action: int
        number of movements per training
    duration: float
        time spent training
    weight: float
        user weight

    Methods
    -------
    get_distance(self) -> float
        returns the distance in kilometers
    get_mean_speed(self) -> float
        returns the average speed of movement
    get_spent_calories() -> float
        returns the number of calories spent
    show_training_info() -> InfoMessage:
        returns an instance of the class InfoMessage
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """
        Sets all the necessary attributes for the object.


        Parameters
        ----------
        action: int
            number of movements per training
        duration: float
            time spent training
        weight: float
            user weight
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get the distance in kilometers."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        raise NotImplementedError(
            'Method "get_spent_calories" in class '
            f'"{type(self).__name__}" not defined')

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed training."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """
    Class describing the type of training: Running.

    ...

    Attributes
    ----------
    RATIO_SPEED: int
        first coefficient unknown to science
    RATIO_SPEED_SHIFT: float
        second coefficient unknown to science

    Methods
    -------
    get_spent_calories() -> float
        redefined method of the base class
    """

    RATIO_SPEED: int = 18
    RATIO_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        return (
            (self.RATIO_SPEED * self.get_mean_speed()
             + self.RATIO_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * (self.duration * self.MIN_IN_HR)
        )


class SportsWalking(Training):
    """
    Class describing the type of training: SportsWalking.


    ...

    Attributes
    ----------
    RATIO_WEIGHT_USER: float
        coefficient from the formula
    RATIO_WEIGHT_SPEED_USER: float
        coefficient from the formula
    KMH_IN_MSEC: float
        the number for converting kilometers per hour to meters per second
    CM_IN_M: int
        number of centimeters per meter
    action: int
        number of movements per training
    duration: float
        time spent training
    weight: float
        user weight
    height: float
        user height in meters

    Methods
    -------
    get_spent_calories()
        redefined method of the base class
    """

    RATIO_WEIGHT_USER: float = 0.035
    RATIO_WEIGHT_SPEED_USER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """
        Sets attributes from the base class and adds its own.


        Parameters
        ----------
        action: int
            number of movements per training
        duration: float
            time spent training
        weight: float
            user weight
        height: float
            user height in meters
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Get the number of calories consumed."""
        return (
            (self.RATIO_WEIGHT_USER * self.weight + (((self.get_mean_speed()
             * self.KMH_IN_MSEC)**2) / (self.height / self.CM_IN_M))
             * self.RATIO_WEIGHT_SPEED_USER * self.weight)
            * (self.duration * self.MIN_IN_HR)
        )


class Swimming(Training):
    """
    Class describing the type of training: Swimming.


    ...

    Attributes
    ----------
    LEN_STEP: float
        length of one stroke when swimming
    SHIFT_MEAN_SPEED: float
        velocity displacement coefficient
    FACTOR: int
        another coefficient
    action: int
        number of movements per training
    duration: float
        time spent training
    weight: float
        user weight
    length_pool: int
        pool length
    count_pool: int
        number of swimming pool crossings

    Methods
    -------
    get_mean_speed() -> float
        redefined method of the base class
    get_spent_calories() -> float
        redefined method of the base class
    """

    LEN_STEP: float = 1.38
    SHIFT_MEAN_SPEED: float = 1.1
    FACTOR: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        """
        Sets attributes from the base class and adds its own.


        Parameters
        ----------
        action: int
            number of movements per training
        duration: float
            time spent training
        weight: float
            user weight
        length_pool: int
            pool length
        count_pool: int
            number of swimming pool crossings
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get the average swimming speed."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        return (
            (self.get_mean_speed() + self.SHIFT_MEAN_SPEED)
            * self.FACTOR * self.weight * self.duration
        )


def read_package(workout_type: str, data: list[int]) -> Union[Running,
                                                              Swimming,
                                                              SportsWalking]:
    """
    Simulation of receiving data from sensors.

    LocalVariable:
    types_training: dict that stores code designations and class references

    Arguments:
    workout_type: training code designation
    data: list with training data

    Raises:
    KeyError: checking for the presence of a key in the dictionary

    Returns:
    instance of the class
    """
    types_training: dict[
        str, type[Union[Running, Swimming, SportsWalking]]
    ] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return types_training[workout_type](*data)
    except KeyError:
        raise KeyError


def main(training: Union[Running, Swimming, SportsWalking]) -> None:
    """
    Main function.

    Arguments:
    training: accepts an instance of the class

    LocalVariable:
    info: instance class InfoMessage

    Returns:
    None
    """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
