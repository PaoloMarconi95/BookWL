class CrossFitClass:
    def __init__(self, id, name, date, time, program):
        self.id = id
        self.name = name
        self.date = date
        self.time = time
        self.program = program

    def __str__(self):
        return f"CrossFitClass: id = {self.id}; name = {self.name}; date = {self.date}; time = {self.time}; program = {self.program}"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_create_user_query(cls, name, mail, password):
        return f"INSERT INTO CROSSFIT_CLASS (name, mail, password) VALUES ({name}, {mail}, {password})"

    @classmethod
    def get_users_query(cls):
        return f"SELECT * FROM CROSSFIT_CLASS"

    @classmethod
    def get_user_by_id_query(cls, class_id):
        return f"SELECT * FROM CROSSFIT_CLASS WHERE id = {class_id}"

    @classmethod
    def map_query_to_class(cls, query_output):
        if len(query_output) != 5:
            raise Exception(f'Cannot map object {query_output} to class CrossFitClass')
        
        return cls(query_output[0], query_output[1], query_output[2], query_output[3], query_output[4])
