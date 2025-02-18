from data_sensor import DataSensor
from controller import Controller
from threading import Thread
import time

if __name__ == '__main__':
    data_sensor = DataSensor()
    controller = Controller()

    def update_controller():
        while True:
            humidity, ph = data_sensor.get_humidity_ph()
            controller.set_humidity_ph(humidity, ph)
            time.sleep(1) 

    try:
        data_sensor_thread = Thread(target=data_sensor.start, daemon=True)
        data_sensor_thread.start()

        update_thread = Thread(target=update_controller, daemon=True)
        update_thread.start()

        controller.run()
    except KeyboardInterrupt:
        data_sensor.stop()
        data_sensor_thread.join()
        update_thread.join()
