from opensky_api import OpenSkyApi
import pandas as pd
from time import time, sleep

# Load Open Sky's API
api = OpenSkyApi()

df_large = pd.DataFrame(columns=["icao24", "callsign", "origin_country", "time_position",
            "last_contact", "longitude", "latitude", "baro_altitude", "on_ground",
            "velocity", "heading", "vertical_rate", "sensors",
            "geo_altitude", "squawk", "spi", "position_source", "fetch_time"])

batch_no = 0
hours = 24
stop_time = time() + 60*60*hours

tolerance = 150 / 60

# For KEDW:
latitude = 34.9240
longitude = -117.8912

# For KNFL:
#latitude = 39.4204
#longitude = -118.7242

# For KNTU:
latitude = 36.8124
longitude = -76.0248


while (time() < stop_time):
    sleep(40)
    
    # Creating batch to avoid memory issues
    df_batch = pd.DataFrame(columns=["icao24", "callsign", "origin_country", "time_position",
            "last_contact", "longitude", "latitude", "baro_altitude", "on_ground",
            "velocity", "heading", "vertical_rate", "sensors",
            "geo_altitude", "squawk", "spi", "position_source", "fetch_time"])

    # Using a try-catch encasement to try to increase api requests
    try:
        # Calling API to receive states within 2.5 degrees (long + lat) box outside DFW, or 150 nautical miles
        # Note: DFW is at lat: 32.8998 long: -97.0403
        # s = api.get_states(bbox=(30.3998, 35.3998, -99.5403, -94.5403))

        # For KRNO airport
        # Note: KRNO is lat: 39.4996 long: -119.7681
        #s = api.get_states(bbox=(36.9996, 41.9996, -122.2681, -117.2681))
        #s = api.get_states()
        
        s = api.get_states(bbox=(latitude - tolerance, latitude + tolerance, longitude - tolerance, longitude + tolerance))

        for b in s.states:
            new_row = [b.icao24, b.callsign, b.origin_country, b.time_position,
                b.last_contact, b.longitude, b.latitude, b.baro_altitude, b.on_ground,
                b.velocity, b.heading, b.vertical_rate, b.sensors,
                b.geo_altitude, b.squawk, b.spi, b.position_source, s.time]
            df_large.loc[len(df_large)] = new_row
            df_batch.loc[len(df_batch)] = new_row

        #batch_name = '../flight_data/KNTU-01-26-22-7AM-24HRS/' + str(batch_no) # TODO: Remove date here
        #df_batch.to_csv(batch_name, index=False)
        batch_no += 1
    except:
        sleep(60)

    

#df_large.to_csv('KEDW-01-29-22-7AM-24HRS', index=False)
#df_large.to_csv('KNFL-01-29-22-7AM-24HRS', index=False)
df_large.to_csv('KNTU-01-29-22-7AM-24HRS', index=False)