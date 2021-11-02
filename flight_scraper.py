from opensky_api import OpenSkyApi
import pandas as pd
from time import time, sleep

# Load Open Sky's API
api = OpenSkyApi()

df = pd.DataFrame(columns=["icao24", "callsign", "origin_country", "time_position",
            "last_contact", "longitude", "latitude", "baro_altitude", "on_ground",
            "velocity", "heading", "vertical_rate", "sensors",
            "geo_altitude", "squawk", "spi", "position_source", "fetch_time"])


while (time() > 1635863347) and (time() < 1635877747):
    sleep(20)
    s = api.get_states(bbox=(31.8998, 33.8998, -98.0403, -96.0403))
    for b in s.states:
        new_row = [b.icao24, b.callsign, b.origin_country, b.time_position,
            b.last_contact, b.longitude, b.latitude, b.baro_altitude, b.on_ground,
            b.velocity, b.heading, b.vertical_rate, b.sensors,
            b.geo_altitude, b.squawk, b.spi, b.position_source, s.time]
        df.loc[len(df)] = new_row
    print(df.tail())

df.to_csv('11_2_6-30_12-30.csv', index=False)