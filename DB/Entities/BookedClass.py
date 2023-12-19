from DB.Database import Database
from datetime import datetime, timedelta
from Config import CONFIG, LOGGER

class BookedClass:
    def __init__(self, user_id, class_id):
        self.user_id = int(user_id)
        self.class_id = int(class_id)

    def __str__(self):
        return f"BookedClass: user_id = {self.user_id}; class_id = {self.class_id}"
    
    def __repr__(self):
        return self.__str__()    
    
    @classmethod
    def get_booked_class_by_user_id_for_current_datetime(cls, user_id):
        query = cls._get_booked_class_by_user_id_query_for_current_datetime(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)


    @classmethod
    def _get_booked_class_by_user_id_query_for_current_datetime(cls, user_id):
        time_strings = []
        for i in range(0, CONFIG.sign_in_delta + 1):
            time_strings.append(f"'{(datetime.now() + timedelta(minutes=i)).strftime('%H:%M')}'")
        
        time_string = ','.join(time_strings)
        LOGGER.info(f"looking for booked class within these time: {time_string} ")
        return f"SELECT user_id, class_id FROM BOOKED_CLASS WHERE user_id = {user_id} and is_signed_in = 0" \
             f" and class_time in({time_string}) and class_date = '{datetime.now().strftime('%Y-%m-%d')}'"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 2:
                raise Exception(f'Cannot map object {output} to class BookedClass')
            parsed_objects.append(cls(output[0], output[1]))
            
        return parsed_objects