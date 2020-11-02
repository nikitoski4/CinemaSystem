from typing import Optional


class Cinema:
    """Класс кинотеатра"""

    def __init__(self,
                 title: str,
                 *args,
                 **kwargs):
        self.title = title

    def add_cinema_hall_to_this_cinema(self, *args, **kwargs):
        pass

    def delete_cinema_hall_from_this_cinema(self, *args):
        pass


class CinemaHall:
    """Класс кинозала"""

    def __init__(self,
                 parent: Cinema,
                 title: str,
                 *args,
                 **kwargs):
        self.parent = parent
        self.title = title

    def add_film_to_this_cinema_hall(self, *args, **kwargs):
        pass

    def delete_film_from_this_cinema_hall(self, *args):
        pass


class Film:
    """Класс киносеанса"""

    def __init__(self,
                 parent: CinemaHall,
                 title: str,
                 *args,
                 description: Optional[str] = '',
                 **kwargs):
        self.parent = parent
        self.title = title
