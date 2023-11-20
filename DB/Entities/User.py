class User:
    def __init__(self, id, name, mail, password):
        self.id = id
        self.name = name
        self.mail = mail
        self.password = password

    def __str__(self):
        return f"User: id = {self.id}; name = {self.name}; mail = {self.mail}; password = {self.password}"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_create_user_query(cls, name, mail, password):
        return f"INSERT INTO USER (name, mail, password) VALUES ({name}, {mail}, {password})"

    @classmethod
    def get_users_query(cls):
        return f"SELECT * FROM USER"

    @classmethod
    def get_user_by_id_query(cls, user_id):
        return f"SELECT * FROM USER WHERE id = {user_id}"

    @classmethod
    def map_query_to_class(cls, query_output):
        if len(query_output) != 4:
            raise Exception(f'Cannot map object {query_output} to class User')
        
        return cls(query_output[0], query_output[1], query_output[2], query_output[3])
