from Enum.WeekDay import WeekDay
from DB.Database import Database
from datetime import datetime, timedelta

class FutureBooking:
    def __init__(self, user_id, class_name, class_program, class_time, week_day):
        self.user_id = int(user_id)
        self.class_name = class_name
        self.class_time = class_time
        self.class_program = class_program
        self.week_day = int(week_day)
        # Human-readable weekday
        self.week_day_string = WeekDay(int(week_day))
        self.class_date = self.date_for_next_week(self.week_day)

    def __str__(self):
        return f"FutureBooking: user_id = {self.user_id}; class_name = {self.class_name}; class_time = {self.class_time}; week_day = {self.week_day};"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def get_future_booking_by_user_id(cls, user_id):
        query = cls._get_future_booking_by_user_id_query(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    
    @classmethod
    def create_future_booking(cls, future_booking):
        query = cls._get_create_future_booking_query(future_booking)
        id = Database.execute_create_query(query)
        return id

    @classmethod
    def _get_create_future_booking_query(cls, future_booking):
        return f"INSERT INTO FUTURE_BOOKING (class_name, class_program, class_time, week_day) VALUES \
            {future_booking.class_name}, {future_booking.class_program}, {future_booking.class_time}, {future_booking.week_day}"

    @classmethod
    def _get_future_bookings_query(cls):
        return f"SELECT user_id, class_name, class_program, class_time, week_day FROM FUTURE_BOOKING"

    @classmethod
    def _get_future_booking_by_user_id_query(cls, user_id):
        return f"SELECT user_id, class_name, class_program, class_time, week_day FROM FUTURE_BOOKING WHERE user_id = {user_id}"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 5:
                raise Exception(f'Cannot map object {output} to class FutureBooking')
            parsed_objects.append(cls(output[0], output[1], output[2], output[3], output[4]))
            
        return parsed_objects
    
    @classmethod
    def date_for_next_week(cls, week_day):
        today = datetime.now()
        current_weekday = today.weekday()

        delta_days = (week_day - current_weekday) % 7
        if delta_days == 0:  # Se il giorno corrente è lo stesso della richiesta, aggiungi 7 giorni per ottenere la prossima data
            delta_days += 7

        next_week_weekday = today + timedelta(days=delta_days)
        return next_week_weekday.strftime("%d-%m-%Y")
    

