import datetime


class CrossFitClass:
    def __init__(self, name: str, datetime: datetime, program: str, id: int = -1, is_booked: bool = False,
                 is_waitlisted: bool = False):
        self.name: str = name
        self.datetime: datetime = datetime
        self.program = program
        self.id: int = id
        self.is_booked: bool = is_booked
        self.is_waitlisted: bool = is_waitlisted

    def __str__(self):
        return f"CrossFitClass: id = {self.id}; name = {self.name}; date = {self.datetime}; program = {self.program}"

    def __repr__(self):
        return self.__str__()