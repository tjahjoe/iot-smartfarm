from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class Model:
    def __init__(self):
        self.__uri = 'mongodb+srv://elchilz:Elco1001@smartfarm.zrqtr.mongodb.net/?retryWrites=true&w=majority&appName=smartfarm'

        self.__client = MongoClient(self.__uri, server_api=ServerApi('1'))

        self.__last_inserted_hour = None

        database_name = 'smartfarm'
        collection_soil = 'soil'
        collection_users = 'users'

        self.__on_connect(database_name, collection_soil, collection_users)

    def __on_connect(self, database_name, collection_soil, collection_users):
        try:
            self.__database = self.__client.get_database(database_name)
            self.__soil = self.__database.get_collection(collection_soil)
            self.__users = self.__database.get_collection(collection_users)

        except Exception as e:
            print(f'Error: {e}')

    def login(self, username, password):
        data = {
            '_id' : username
        }
        user = self.__users.find_one(data)

        if not user:
            return 'failed'
        
        if check_password_hash(user['password'], password):
            return 'success'
        else:
            return 'failed'

    def regrister(self, username, password):
        try:
            hashed_password = generate_password_hash(password)

            data = {
                '_id' : username,
                'password' : hashed_password
            }
            self.__users.insert_one(data)
            
            return 'success'
        except DuplicateKeyError:
            return 'failed'



    def insert_soil(self, humidity, ph):
        now = datetime.now()
        hour = now.hour

        if self.__last_inserted_hour != hour:
            year = now.year
            month = now.month
            day = now.day

            data = {
                'day' : day,
                'month' : month,
                'year' : year,
                'humidity' : humidity,
                'ph' : ph
            }

            self.__soil.insert_one(data)

            self.__last_inserted_hour = hour

    