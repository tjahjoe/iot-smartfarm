import paho.mqtt.client as mqtt
import json 

class DataSensor:
    def __init__(self):
        self.__BROKER = 'broker.emqx.io'
        self.__PORT = 8084 
        self.__USERNAME = 'chilz'
        self.__PASSWORD = 'chilz123'
        self.__TOPIC = 'UNI142/NgulikBoys/aktuasi_led'  
        self.__QOS = 0

        self.__client = mqtt.Client(transport='websockets')
        self.__mqtt_configuration()

        self.__humidity = 0
        self.__ph = 0

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.__client.subscribe(self.__TOPIC, self.__QOS)
            print('Connected to MQTT Broker')
    
    def __on_message(self, client, userdata, msg):
        try:
            message = json.loads(msg.payload.decode())
            self.__humidity = float(message.get('humidity', 0)) or 0
            self.__ph = float(message.get('ph', 0)) or 0
            print(f'Humidity: {self.__humidity}, pH: {self.__ph}')
        except Exception as e:
            print(f'Error: {e}')

    def __on_disconnect(self, client, userdata, rc):
        if rc == 0:
            print('Disconnected')

    def __mqtt_configuration(self):
        self.__client.username_pw_set(self.__USERNAME, self.__PASSWORD)
        self.__client.tls_set()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.on_disconnect = self.__on_disconnect
        
    def start(self):
        self.__client.reconnect_delay_set(min_delay=1, max_delay=120)
        self.__client.connect(self.__BROKER, self.__PORT, 60)
        self.__client.loop_forever()
    
    def stop(self):
        self.__client.disconnect()
    
    def get_humidity_ph(self):
        return self.__humidity, self.__ph
