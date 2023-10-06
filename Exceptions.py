class NoReservationFoundException(Exception):
    pass


class GlobalVariablesNotSetException(Exception):
    pass


class ClassNotFoundWithinDropDownException(Exception):

    def __init__(self, class_name, message='Class not found within dropdown with value '):
        self.salary = class_name
        self.message = message + class_name
        super().__init__(self.message)
