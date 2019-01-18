from os import environ
from time import sleep
from libtado.api import Tado
from prometheus_client import start_http_server, Gauge

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    username = environ["TADO_USERNAME"]
    password = environ["TADO_PASSWORD"]
    client_secret = environ["TADO_CLIENT_SECRET"]
    # 3 minutes seems the default tado app value
    refresh_rate = int(environ.get("TADO_EXPORTER_REFRESH_RATE", 180))
    print("Starting tado exporter")
    start_http_server(8000)
    print("Connecting to tado API using account " + username)
    tado = Tado(username, password, client_secret)
    temp = Gauge('tado_temperature', 'Temperature as read by the sensor', 
                  labelnames=['zone_name'],
                  unit='celsius')
    humi = Gauge('tado_humidity', 'Humidity as read by the sensor', 
                  labelnames=['zone_name'],
                  unit='percentage')
    print("Exporter ready")
    while True:
        temp.labels('zone1').set(tado.get_state(1)['sensorDataPoints']['insideTemperature']['celsius'])
        humi.labels('zone1').set(tado.get_state(1)['sensorDataPoints']['humidity']['percentage'])
        # TODO: implement a drift-free loop
        sleep(refresh_rate)
