from flask import Flask, request, jsonify
from flask_cors import CORS
from model import Model

class Controller:
    def __init__(self):
        self._app = Flask(__name__)
        CORS(self._app)
        self.__model = Model()

        self.__humidity = 0
        self.__ph = 0

        self.__humidity_history = []
        self.__ph_history = []

        self._app.add_url_rule('/data', view_func=self._data, methods=['GET'])
        self._app.add_url_rule('/login', view_func=self._login, methods=['POST'])
        self._app.add_url_rule('/regrister', view_func=self._regrister, methods=['POST'])
    
    def set_humidity_ph(self, humidity, ph):
        self.__humidity = humidity
        self.__ph = ph

        if len(self.__humidity_history) == 8:
            self.__humidity_history = self.__humidity_history[1:]
        if len(self.__ph_history) == 8:
            self.__ph_history = self.__ph_history[1:]

        self.__humidity_history.append(humidity) 
        self.__ph_history.append(ph)

        self.__model.insert_soil(humidity, ph)

    def _data(self):
        # return jsonify({
        #     "humidity": self.__humidity_history,
        #     "ph": self.__ph_history
        # })
        return jsonify({
            'humidity' : self.__humidity,
            'ph' : self.__ph
        })
    
    def _login(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        result = self.__model.login(username, password)
        return jsonify({"message": result})

    def _regrister(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        result = self.__model.regrister(username, password)
        return jsonify({"message": result})

    def run(self):
        self._app.run(host='0.0.0.0')
