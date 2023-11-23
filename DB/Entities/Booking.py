from DB.Entities import DB

class Booking:
    def __init__(self, user_id, class_id, is_signed_in):
        self.user_id = user_id
        self.class_id = class_id
        self.is_signed_in = is_signed_in

    def __str__(self):
        return f"Booking: user_id = {self.user_id}; class_id = {self.class_id}; is_signed_in = {self.is_signed_in};"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def get_every_booking_by_user_id(cls, user_id):
        query = cls._get_booking_by_user_id_query(user_id)
        result = DB.execute_query(query)
        return cls._map_query_to_class(result)

    @classmethod
    def create_booking(cls, booking):
        query = cls._get_create_booking_query(booking)
        DB.execute_query(query)
        return DB.cur.lastrowid

    @classmethod
    def _get_create_booking_query(cls, booking):
        return f"INSERT INTO BOOKING (user_id, class_id, is_signed_in) VALUES \
            ({booking.user_id}, {booking.class_id}, {DB.convert_boolean(booking.is_signed_in)})"

    @classmethod
    def _get_bookings_query(cls):
        return f"SELECT * FROM BOOKING"

    @classmethod
    def _get_booking_by_user_id_query(cls, user_id):
        return f"SELECT * FROM BOOKING WHERE user_id = {user_id}"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 3:
                raise Exception(f'Cannot map object {output} to class Booking')
            parsed_objects.append(cls(output[0], output[1], output[2]))
            
        return parsed_objects