from DB.Entities import DB

class CrossFitClass:
    def __init__(self, name, date, time, program, id=None):
        self.name = name
        self.date = date
        self.time = time
        self.program = program
        self.id = id

    def __str__(self):
        return f"CrossFitClass: id = {self.id}; name = {self.name}; date = {self.date}; time = {self.time}; program = {self.program}"
    
    def __repr__(self):
        return self.__str__()
    

    @classmethod
    def get_every_crossfit_class_by_user_id(cls, user_id):
        query = cls._get_crossfit_class_by_user_id_query(user_id)
        result = DB.execute_query(query)
        return cls._map_query_to_class(result)

    @classmethod
    def create_crossfit_class(cls, crossfit_class):
        query = cls._get_create_crossfit_class_query(crossfit_class)
        DB.execute_query(query)
        return DB.cur.lastrowid

    @classmethod
    def _get_create_crossfit_class_query(cls, crossfit_class):
        return f"INSERT INTO CROSSFIT_CLASS (name, program, date, time) VALUES  \
            ('{crossfit_class.name}', '{crossfit_class.program}', {DB.convert_date(crossfit_class.date)}, '{crossfit_class.time}')"

    @classmethod
    def _get_crossfit_class_by_user_id_query(cls, user_id):
        return f"SELECT * FROM CROSSFIT_CLASS WHERE user_id = {user_id}"

    @classmethod
    def _get_crossfit_classes_query(cls):
        return f"SELECT * FROM CROSSFIT_CLASS"
    

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 5:
                raise Exception(f'Cannot map object {output} to class CrossFitClass')
            parsed_objects.append(cls(output[0], output[1], output[2], output[3], output[4]))
            
        return parsed_objects
