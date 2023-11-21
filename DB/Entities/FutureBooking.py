class FutureBooking:
    def __init__(self, user_id, class_name, class_time, week_day):
        self.user_id = user_id
        self.class_name = class_name
        self.class_time = class_time
        self.week_day = week_day

    def __str__(self):
        return f"FutureBooking: user_id = {self.user_id}; class_name = {self.class_name}; class_time = {self.class_time}; week_day = {self.week_day};"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_create_future_booking_query(cls, name, mail, password):
        return f"INSERT INTO FUTURE_BOOKING (name, mail, password) VALUES ({name}, {mail}, {password})"

    @classmethod
    def get_future_bookings_query(cls):
        return f"SELECT * FROM FUTURE_BOOKING"

    @classmethod
    def get_future_booking_by_id_query(cls, user_id):
        return f"SELECT * FROM FUTURE_BOOKING WHERE id = {user_id}"

    @classmethod
    def map_query_to_class(cls, query_output):
        if len(query_output) != 4:
            raise Exception(f'Cannot map object {query_output} to class FutureBooking')
        
        return cls(query_output[0], query_output[1], query_output[2])
