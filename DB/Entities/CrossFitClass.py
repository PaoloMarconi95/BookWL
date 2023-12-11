from DB.Database import Database
from Config import LOGGER

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
    

    def exists(self):
        query = self._get_crossfit_class_by_crossfit_class(self)
        result = Database.execute_query(query)
        if len(result) == 1:
            return True
        elif len(result) == 0:
            return False
        else:
            raise Exception(f"Tried to retrieva max 1 CrossFitClass for exists() method but i got {str(len(result))} results")  

    def retrive_id(self):
        query = self._get_crossfit_class_by_crossfit_class(self)
        result = Database.execute_query(query)
        return CrossFitClass._map_query_to_class(result)[0].id

    """
    :params None
    Insert the CrossFitClass if not present in the DB, 
    :returns the CrossFitClass id if already present
    """
    def upsert(self):
        if self.exists():
            return self.retrive_id()
        else:
            LOGGER.info(f"Found that class {self} does not exists within db! inserting it...")
            return CrossFitClass.create_crossfit_class(self)

    @classmethod
    def get_every_crossfit_class_by_user_id(cls, user_id):
        query = cls._get_crossfit_class_by_user_id_query(user_id)
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)

    @classmethod
    def create_crossfit_class(cls, crossfit_class):
        query = cls._get_create_crossfit_class_query(crossfit_class)
        id = Database.execute_create_query(query)
        return id
    
    @classmethod
    def get_crossfit_class_by_id(cls, class_id):
        query = cls._get_crossfit_class_by_id_query(class_id)
        result = Database.execute_query(query)
        result = cls._map_query_to_class(result)
        if len(result) == 1:
            return result[0]
        elif len(result) == 0:
            raise Exception(f"No crossfit class found for id {str(class_id)}")
        else:
            raise Exception(f"Too many crossfit class found for id {str(class_id)}")


    @classmethod
    def _get_create_crossfit_class_query(cls, crossfit_class):
        return f"INSERT INTO CROSSFIT_CLASS (name, program, date, time) VALUES  \
            ('{crossfit_class.name}', '{crossfit_class.program}', {Database.convert_date(crossfit_class.date)}, '{crossfit_class.time}')"

    @classmethod
    def _get_crossfit_class_by_user_id_query(cls, user_id):
        return f"SELECT name, date, time, program, id FROM CROSSFIT_CLASS WHERE user_id = {user_id}"

    @classmethod
    def _get_crossfit_class_by_id_query(cls, class_id):
        return f"SELECT name, date, time, program, id FROM CROSSFIT_CLASS WHERE id = {class_id}"
    
    @classmethod
    def _get_crossfit_class_by_crossfit_class(cls, crossfit_class):
        return f"SELECT name, date, time, program, id FROM CROSSFIT_CLASS WHERE name = '{crossfit_class.name}' and date = {Database.convert_date(crossfit_class.date)} \
            and time = '{crossfit_class.time}' AND program = '{crossfit_class.program}'"
    

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 5:
                raise Exception(f'Cannot map object {output} to class CrossFitClass')
            parsed_objects.append(cls(output[0], output[1], output[2], output[3], output[4]))
            
        return parsed_objects
