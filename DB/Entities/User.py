from DB.Database import Database
import pickle
import os
import time

# Custom
from Config import CONFIG, LOGGER
from Tasks.SafeAccess import safe_access

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class User:
    def __init__(self, id, name, mail, password):
        self.id = id
        self.name = name
        self.mail = mail
        self.password = password
        self.is_logged_in = False
        self.cookies_loaded = False
        self.cookies_file = os.path.join(CONFIG.cookie_path, f"{name}_cookies.pkl")

    def __str__(self):
        return f"User: id = {self.id}; name = {self.name}; mail = {self.mail}; password = {self.password}"
    
    def __repr__(self):
        return self.__str__()
    
    def login(self, wd) -> bool:
        attempts = 0
        while not self.is_logged_in and attempts < CONFIG.max_login_attempts:
            try:
                logged_in = self.perform_login(wd)
            except AttributeError as e:
                LOGGER.error(f'Login for user {self.name} failed! ({e}) Trying again...')
            finally:
                attempts += 1
        
        return logged_in
    

    def load_cookies(self):
        LOGGER.info("Loading cookies..")
        with open(self.cookies_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
    
    def save_cookies(self):
        # Salva i cookie utilizzando pickle
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, "wb") as f:
            pickle.dump(cookies, f)


    def perform_login(self, wd):
        if(os.path.isfile(self.cookies_file)):
            self.load_cookies()
        wd.get(CONFIG.calendar_url)
        login_el = safe_access(wd, 'FormLogin')
        LOGGER.info("Login form recognized")
        username_el = login_el.find_element(By.ID, 'Input_UserName')
        username_el.send_keys(self.mail)
        pwd_el = login_el.find_element(By.ID, 'Input_Password')
        pwd_el.send_keys(self.password)
        submit_el = login_el.find_element(By.TAG_NAME, 'button')
        submit_el.click()
        LOGGER.info("sign-in button clicked, now waiting for main calendar page to be rendered")

        calendar_el = None
        try:
            calendar_el = safe_access(wd, CONFIG.calendar_el_id)
        except Exception as e:
            LOGGER.error(str(e))

        if calendar_el is not None:
            LOGGER.info(f'User {self.name} successfully logged in!')
            self.is_logged_in = True
            self.save_cookies()

    def log_out(self, wd):
        LOGGER.info(f"Logging out {self.name}")
        logout_el = WebDriverWait(wd, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Logout"]'))
        )
        logout_el.click()
        LOGGER.info(f"Log out for {self.name} completed")
        self.is_logged_in = False


    # Static methods        

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
    
