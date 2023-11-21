class Booking:
    def __init__(self, user_id, class_name, is_logged_in):
        self.user_id = user_id
        self.class_id = class_id
        self.is_logged_in = is_logged_in

    def __str__(self):
        return f"Booking: user_id = {self.user_id}; class_id = {self.class_id}; is_logged_in = {self.is_logged_in};"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_create_booking_query(cls, name, mail, password):
        return f"INSERT INTO BOOKING (name, mail, password) VALUES ({name}, {mail}, {password})"

    @classmethod
    def get_bookings_query(cls):
        return f"SELECT * FROM BOOKING"

    @classmethod
    def get_booking_by_user_id_query(cls, user_id):
        return f"SELECT * FROM BOOKING WHERE user_id = {user_id}"

    @classmethod
    def map_query_to_class(cls, query_output):
        if len(query_output) != 3:
            raise Exception(f'Cannot map object {query_output} to class Booking')
        
        return cls(query_output[0], query_output[1], query_output[2])