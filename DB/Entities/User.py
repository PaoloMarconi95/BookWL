from DB.Database import Database

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
    def get_every_users(cls):
        query = cls._get_users_query()
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)
    
    @classmethod
    def get_user_by_id(cls, user_id):
        query = cls._get_user_by_id_query(user_id)
        result = Database.execute_query(query)
        user = cls._map_query_to_class(result)
        if len(user) == 1:
            return user[0]
        elif len(user) > 1:
            raise Exception(f"More than 1 user found for id {user_id}!")
        else:
            raise Exception(f"No user found for id {user_id}!")
    
    @classmethod
    def get_every_users(cls):
        query = cls._get_users_query()
        result = Database.execute_query(query)
        return cls._map_query_to_class(result)

    @classmethod
    def _get_users_query(cls):
        return f"SELECT * FROM USER"

    @classmethod
    def _get_user_by_id_query(cls, user_id):
        return f"SELECT * FROM USER WHERE id = {user_id}"

    @classmethod
    def _map_query_to_class(cls, query_output):
        parsed_objects = []
        for output in query_output:
            if len(output) != 4:
                raise Exception(f'Cannot map object {output} to class User')
            parsed_objects.append(cls(output[0], output[1], output[2], output[3]))
            
        return parsed_objects
    
