from DB.Database import Database
from datetime import datetime, timedelta
from Config import CONFIG, LOGGER

class Booking:
    def __init__(self, user_id, class_id, is_signed_in, time):
        self.user_id = int(user_id)
        self.class_id = int(class_id)
        self.is_signed_in = True if is_signed_in == 1 else 0
        self.time = time

    def __str__(self):
        return f"Booking: user_id = {self.user_id}; class_id = {self.class_id}; is_signed_in = {self.is_signed_in};"
    
    def __repr__(self):
        return self.__str__()
    
    def set_as_signed_in(self):
        query = self._get_update_signed_in_crossfit_class_query(self)
        Database.execute_query(query, commit=True)
        self.is_signed_in = True

    
    @classmethod
    def get_every_active_booking_by_user_id(cls, user_id):
        query = cls._get_active_booking_by_user_id_query(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    
    
    @classmethod
    def get_active_booking_by_user_id_for_current_time(cls, user_id):
        query = cls._get_active_booking_by_user_id_query_for_current_time(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    

    @classmethod
    def create_booking(cls, booking):
        query = cls._get_create_booking_query(booking)
        id = Database.execute_create_query(query)
        return id

    @classmethod
    def _get_create_booking_query(cls, booking):
        return f"INSERT INTO BOOKING (user_id, class_id, is_signed_in, time) VALUES \
            ({booking.user_id}, {booking.class_id}, {Database.convert_boolean(booking.is_signed_in)}, '{booking.time}')"

    @classmethod
    def _get_bookings_query(cls):
        return f"SELECT * FROM BOOKING"

    @classmethod
    def _get_active_booking_by_user_id_query(cls, user_id):
        return f"SELECT * FROM BOOKING WHERE user_id = {user_id} and is_signed_in = 0"

    @classmethod
    def _get_active_booking_by_user_id_query_for_current_time(cls, user_id):
        time_strings = []
        for i in range(0, CONFIG.sign_in_delta):
            time_strings.append(f"'{(datetime.now() + timedelta(minutes=i)).strftime('%H:%M')}'")
        
        time_string = ','.join(time_strings)
        LOGGER.info(f"looking for bookable class within these time: {time_string} ")
        return f"SELECT * FROM BOOKING WHERE user_id = {user_id} and is_signed_in = 0 and time in({time_string})"
    
        
    @classmethod
    def _get_update_signed_in_crossfit_class_query(cls, booking):
        return f"UPDATE CROSSFIT_CLASS SET is_signed_in = {Database.convert_boolean(booking.is_signed_in)} \
            WHERE class_id = {booking.class_id} and user_id = {booking.user_id}"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 4:
                raise Exception(f'Cannot map object {output} to class Booking')
            parsed_objects.append(cls(output[0], output[1], output[2], output[3]))
            
        return parsed_objects