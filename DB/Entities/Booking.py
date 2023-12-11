from DB.Database import Database
from Config import LOGGER

class Booking:
    def __init__(self, user_id, class_id, is_signed_in):
        self.user_id = int(user_id)
        self.class_id = int(class_id)
        self.is_signed_in = True if is_signed_in == 1 else 0

    def __str__(self):
        return f"Booking: user_id = {self.user_id}; class_id = {self.class_id}; is_signed_in = {self.is_signed_in};"
    
    def __repr__(self):
        return self.__str__()
    
    def set_as_signed_in(self):
        query = self._get_update_signed_in_crossfit_class_query(self)
        Database.execute_query(query, commit=True)
        self.is_signed_in = True

    def exists(self):
        query = self._get_booking_by_booking(self)
        result = Database.execute_query(query)
        if len(result) == 1:
            return True
        elif len(result) == 0:
            return False
        else:
            raise Exception(f"Tried to retrieve 1 CrossFitClass for exists() method but i got {str(len(result))} results") 
        
    def upsert(self):
        if not self.exists():
            LOGGER.info(f"Found that booking {self} does not exists within db! inserting it...")
            return Booking.create_booking(self)

    
    @classmethod
    def get_every_active_booking_by_user_id(cls, user_id):
        query = cls._get_active_booking_by_user_id_query(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    
    
    @classmethod
    def get_booking_by_user_and_class_id(cls, class_id, user_id):
        query = cls._get_booking_by_user_and_class_id_query(class_id, user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    

    @classmethod
    def create_booking(cls, booking):
        query = cls._get_create_booking_query(booking)
        id = Database.execute_create_query(query)
        return id

    @classmethod
    def _get_create_booking_query(cls, booking):
        return f"INSERT INTO BOOKING (user_id, class_id, is_signed_in) VALUES \
            ({booking.user_id}, {booking.class_id}, {Database.convert_boolean(booking.is_signed_in)})"

    @classmethod
    def _get_booking_by_user_and_class_id_query(cls, class_id, user_id):
        return f"SELECT user_id, class_id, is_signed_in FROM BOOKING where class_id = {class_id} and user_id = {user_id}"

    @classmethod
    def _get_active_booking_by_user_id_query(cls, user_id):
        return f"SELECT user_id, class_id,is_signed_in FROM BOOKING WHERE user_id = {user_id} and is_signed_in = 0"

    @classmethod
    def _get_booking_by_booking(cls, booking):
        return f"SELECT user_id, class_id, is_signed_in FROM BOOKING WHERE user_id = {booking.user_id} and " \
                f" is_signed_in = {Database.convert_boolean(booking.is_signed_in)}" \
                f" and class_id = {booking.class_id}"
        
        
    @classmethod
    def _get_update_signed_in_crossfit_class_query(cls, booking):
        return f"UPDATE CROSSFIT_CLASS SET is_signed_in = {Database.convert_boolean(booking.is_signed_in)}" \
            f" WHERE class_id = {booking.class_id} and user_id = {booking.user_id}"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 4:
                raise Exception(f'Cannot map object {output} to class Booking')
            parsed_objects.append(cls(output[0], output[1], output[2]))
            
        return parsed_objects